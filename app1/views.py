from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from sms.models import SMSReport
from report.models import UserLog
from .forms import BankTransactionForm, CustomerForm, DPSForm, DPSTransactionForm, SavingsTransactionForm, ShareTransactionForm, VoucherTransactionForm
from .models import Customer, DPS, Logo, Package, ShareAC, ShareACTransactionHistory
from .models import SavingsAC, GeneralAC
from primary_setup.models import BankTransaction, DPSScheme, Holiday, SMSSetting, VoucherTransaction
import requests
from django.views.decorators.http import require_POST
from functools import wraps
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from .forms import GeneralTransactionForm
from .utils import verification

from environ import Env
env = Env()
Env.read_env()

sms_url=env('SMS_URL')
api_key = env('API_Key')
client_id = env('Client_ID')
sender_id = env('Sender_ID')
SMS = env('SMS')



def send_sms(**kwargs):

    if SMS != 'on':
        return "SMS notifications are turned off. No SMS was sent."
    
    # print('sending sms...')
    
    number = kwargs.get('number')
    title = kwargs.get('title')
    user = kwargs.get('user')
    account_number = kwargs.get('account_number')
    amount = kwargs.get('amount')
    installment = kwargs.get('installment')
    installment_amount = kwargs.get('installment_amount')
    due = kwargs.get('due')
    balance = kwargs.get('balance')

    last_11_digits = str(number)[-11:]
    number = "88" + last_11_digits
    
    sms = SMSSetting.objects.get(title=title)
    if sms.status == 'off':
        return
    msg = sms.content_bengali


    # Fetch somity_name from the Logo model
    try:
        somity_name = Logo.objects.first().somity_name
    except (Logo.DoesNotExist, AttributeError):
        somity_name = "Unknown Somity"

    msg = msg.replace('[somity_name]', somity_name)
    
    if account_number:
        msg = msg.replace('[account_number]', account_number)
    if amount:
        msg = msg.replace('[amount]', str(amount))
    if installment:
        msg = msg.replace('[installment]', str(installment))
    if installment_amount:
        msg = msg.replace('[installment_amount]', str(installment_amount))
    if due:
        msg = msg.replace('[due]', str(due))
    if balance:
        msg = msg.replace('[balance]', str(balance))
    
    # print('msg:', msg)
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "senderId": sender_id,
        "is_Unicode": True,
        "message": msg,
        "mobileNumbers": number, 
        "apiKey": api_key,
        "clientId": client_id
    }
    response = requests.post(url=sms_url, headers=headers, json=payload)
    # print(response)
    SMSReport.objects.create(
        sms_type=title,
        mobile_number=number,
        sms_body=msg,
        sent_by=user.username
    )
    return msg
    
    
    
def group_check(user):
    return user.is_authenticated and (user.groups.filter(name='admin').exists() or user.groups.filter(name='manager').exists())

def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'is_staff') and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/access-denied/')
    
    return _wrapped_view

def access_denied(request):
    return render(request, 'app1/deny.html')




def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # print('ok')
            login(request, user)
            
            UserLog.objects.create(processed_by=request.user, logs_action='Login', description='User logged in',)
            
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'app1/others/login.html')

@login_required
def signout(request):
    UserLog.objects.create(processed_by=request.user, logs_action='Logout',description='User logged out')
    logout(request)
    return redirect('login')

@staff_required
def home(request):

    date = datetime.now()

    
    return render(request, 'app1/others/home.html', {'date': date})

# @user_passes_test(group_check)
def package(request):
    package = Package.objects.first()
    if not package:
        return render(request, 'app1/package.html', {'error': 'No packages available'})
    
    return render(request, 'app1/package.html', {'package': package})


###################################################################
# Customer

@login_required
def customer_home(request):
    customer = request.user

    dps = DPS.objects.filter(customer=customer)

    share = ShareAC.objects.filter(customer=customer)
    generalAC = get_object_or_404(GeneralAC, customer=customer)
    savingsAC = get_object_or_404(SavingsAC, customer=customer)


    dps_balance = sum(d.total_amount for d in dps)

    share_balance = sum(s.balance for s in share)
    share_profit_balance = sum(s.profit_balance for s in share)

    general_savings = generalAC.balance
    special_savings = savingsAC.balance

    context = {
                'customer': customer,

                'dps_balance': dps_balance,

                'share_balance': share_balance,
                'share_profit_balance': share_profit_balance,
                'general_savings': general_savings,
                'special_savings': special_savings,
                'generalAC': generalAC,
                'shares': share,
                'dpss': dps,

            }
    return render(request, 'app1/customer_home.html', context)

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('customer_home')
        else:
            messages.error(request, 'Invalid credentials or not a customer.')

    # print('ok')
    return render(request, 'app1/customer_login.html')

@login_required
def customer_signout(request):
    # print('ok')
    logout(request)
    return redirect('customer_login')

@login_required
def customer_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = Customer.objects.get(account_number=request.user.account_number)
        except Customer.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('customer_home')

        if user.password == old_password:
            if new_password == confirm_password:
                user.password = new_password  # Store the new password in plain text
                user.save()
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('customer_home')
            else:
                messages.error(request, 'New password and confirmation do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')
    
# Customer
###################################################################




@login_required
@permission_required('auth.view_permission', raise_exception=True)
def manage_permissions(request):
    groups = Group.objects.all()
    permissions = Permission.objects.all().order_by('content_type__app_label', 'codename')

    if request.method == 'POST':
        action = request.POST.get('action')
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id) if group_id else None
        
        if action == "add":
            group_name = request.POST.get('group_name')
            if group_name:
                new_group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    messages.success(request, f"Group '{group_name}' added successfully!")
                else:
                    messages.warning(request, f"Group '{group_name}' already exists.")
            else:
                messages.error(request, "Group name cannot be empty.")

        elif action == 'edit' and group:
            group_name = request.POST.get('group_name')
            if group_name:
                group.name = group_name
                group.save()
                messages.success(request, f"Group name updated to '{group.name}'.")
            else:
                messages.error(request, "Group name cannot be empty.")

        elif action == 'delete' and group:
            group.delete()
            messages.success(request, "Group deleted successfully.")

        elif action == "permissions" and group:
            selected_permissions = request.POST.getlist('permissions')
            print("Selected permissions:", selected_permissions)  # Debugging line
            group.permissions.clear()  # Clear existing permissions
            group.permissions.set(selected_permissions)  # Assign new permissions
            group.save()
            messages.success(request, f"Permissions updated for group '{group.name}'!")


        return redirect('manage_permissions')

    categorized_permissions = {}
    for perm in permissions:
        app_label = perm.content_type.app_label
        if app_label not in categorized_permissions:
            categorized_permissions[app_label] = []
        categorized_permissions[app_label].append(perm)

    context = {
        'groups': groups,
        'categorized_permissions': categorized_permissions
    }
    return render(request, 'permissions.html', context)






###################################################################
# Customer

@login_required
def customer_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save()
            
            sms_msg = send_sms(
                number=customer.customer_mobile,
                title='Add Customer',
                user=request.user,
                account_number=customer.account_number,
            )
            messages.success(request, 'Customer has been added successfully.')
            return redirect('customer_list')
        else:
            print("Form Errors:", form.errors)

    else:
        form = CustomerForm()

    context = {
        'form': form,
    }
    return render(request, 'app1/customer/customer_add2.html', context)

@login_required
def customer_list(request):
    customers = Customer.objects.filter().order_by
    context = {
        'customers': customers,
    }
    return render(request, 'app1/customer/customer_list.html', context)

@login_required
def customer_details(request, id):
    customer = get_object_or_404(Customer, id=id)
    context = {
        'customer': customer,
    }
    return render(request, 'app1/customer/customer_details1.html', context)

@login_required
def customer_edit(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer details have been updated successfully.')
            return redirect('customer_edit', id=customer.id)
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'app1/customer/customer_edit.html', context)

# Customer
################################################################

################################################################
# General AC

@login_required
def general_list(request):

    customers = GeneralAC.objects.filter().order_by('-id')

    return render(request, 'app1/general/general_list.html', {'customers': customers})

@login_required
def general_deposit(request, id):
    account = get_object_or_404(GeneralAC, id=id)

    if request.method == "POST":
        form = GeneralTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = "deposit"

            # Update account balance
            account.total_deposit += transaction.amount
            account.balance += transaction.amount

            account.save()
            transaction.save()

            sms_msg = send_sms(
                    number=account.customer.customer_mobile,
                    title='Deposit General AC',
                    user=request.user,
                    amount=transaction.amount,
                    balance=account.balance,
                    account_number=account.customer.account_number,
                )
            
            messages.success(request, f"Deposit of {transaction.amount} was successful!")
            return redirect('general_deposit', id=id)
    else:
        form = GeneralTransactionForm()

    context = {
        'form': form,
        'data': account,
    }
    return render(request, 'app1/general/general_deposit.html', context)

@login_required
def general_withdraw(request, id):
    account = get_object_or_404(GeneralAC, id=id)

    if request.method == "POST":
        form = GeneralTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = "withdraw"

            if transaction.amount > account.balance:
                messages.error(request, "Insufficient balance for withdrawal.")
                return redirect('general_withdraw', id=id)

            # Update account balance
            account.total_withdraw += transaction.amount
            account.balance -= transaction.amount

            account.save()
            transaction.save()
            
            sms_msg = send_sms(
                number=account.customer.customer_mobile,
                title='Withdraw General AC',
                user=request.user,
                amount=transaction.amount,
                balance=account.balance,
                account_number=account.customer.account_number,
            )

            messages.success(request, f"Withdrawal of {transaction.amount} was successful!")
            return redirect('general_withdraw', id=id)
    else:
        form = GeneralTransactionForm()

    context = {
        'form': form,
        'data': account,
    }
    return render(request, 'app1/general/general_withdraw.html', context)

@login_required
def general_transaction_history(request, id):
    general = GeneralAC.objects.get(id=id)
    transactions = general.general_transaction_history.all().order_by('-id')
    return render(request, 'app1/general/general_transactions.html', {'data': general, 'transactions': transactions})

# General AC
################################################################

################################################################
# Savings AC

@login_required
@permission_required('app1.view_savingsac', raise_exception=True)
def savings_list(request):
    
    customers = SavingsAC.objects.filter().order_by('-id')

    return render(request, 'app1/savings/general_list.html', {'customers': customers})

@login_required
@permission_required('app1.view_savingsdeposit', raise_exception=True)
def savings_deposit(request, id):
    account = get_object_or_404(SavingsAC, id=id)

    if request.method == "POST":
        form = SavingsTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = "deposit"

            # Update account balance
            account.total_deposit += transaction.amount
            account.balance += transaction.amount

            account.save()
            transaction.save()

            sms_msg = send_sms(
                number=account.customer.customer_mobile,
                title='Deposit Savings AC',
                user=request.user,
                amount=transaction.amount,
                balance=account.balance,
                account_number=account.customer.account_number,
            )
            
            messages.success(request, f"Deposit of {transaction.amount} was successful!")
            return redirect('savings_deposit', id=id)
    else:
        form = SavingsTransactionForm()

    context = {
        'form': form,
        'data': account,
    }
    return render(request, 'app1/savings/general_deposit.html', context)

@login_required
@permission_required('app1.view_savingswithdraw', raise_exception=True)
def savings_withdraw(request, id):
    account = get_object_or_404(SavingsAC, id=id)


    if request.method == "POST":
        form = SavingsTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = "withdraw"

            if transaction.amount > account.balance:
                messages.error(request, "Insufficient balance for withdrawal.")
                return redirect('savings_withdraw', id=id)

            # Update account balance
            account.total_withdraw += transaction.amount
            account.balance -= transaction.amount

            account.save()
            transaction.save()
            
            sms_msg = send_sms(
                number=account.customer.customer_mobile,
                title='Withdraw General AC',
                user=request.user,
                amount=transaction.amount,
                balance=account.balance,
                account_number=account.customer.account_number,
            )

            messages.success(request, f"Withdrawal of {transaction.amount} was successful!")
            return redirect('savings_withdraw', id=id)
    else:
        form = SavingsTransactionForm()

    context = {
        'form': form,
        'data': account,
    }
    return render(request, 'app1/savings/general_withdraw.html', context)

@login_required
def savings_transaction_history(request, id):
    general = SavingsAC.objects.get(id=id)
    transactions = general.savings_transaction_history.all().order_by('-id')
    return render(request, 'app1/savings/general_transactions.html', {'data': general, 'transactions': transactions})

# Savings AC
################################################################

################################################################
# DPS

@login_required
@permission_required('app1.add_dps', raise_exception=True)
def dps_search(request):
    return render(request, 'app1/dps/dps_search.html')

@login_required
@permission_required('app1.add_dps', raise_exception=True)
def dps_create(request, account_number):
    try:
        customer = Customer.objects.get(account_number=account_number)

        if request.method == 'POST':
            form = DPSForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.customer = customer
                data.processed_by = request.user
                data.save()
                data.generate_installment_schedule()
                messages.success(request, f"DPS created successfully with Transaction ID {data.transaction_id}.")

                sms_msg = send_sms(
                    number=customer.customer_mobile,
                    title='Add DPS AC',
                    user=request.user,
                    amount=data.dps_opening_charge,
                )
                messages.success(request, sms_msg)
                # UserLog.objects.create(processed_by=request.user,logs_action='Add DPS AC',description=f'Account Number: {customer.account_number}, DPS ID: {data.transaction_id}')
                # UserLog.objects.create(processed_by=request.user,action=f'DPS Opening Charge',amount=data.dps_opening_charge, customer=customer)

                return redirect('dps_list')
            else:
                messages.error(request, "There was an error with the form.")
        else:
            form = DPSForm()

        dps_schemes = list(DPSScheme.objects.values())

        context = {
            'customer': customer,
            'form': form,
            'dps_schemes': dps_schemes,
        }
        return render(request, 'app1/dps/dps_create.html', context)
    except Customer.DoesNotExist:
        messages.error(request, f"No customer found with account number: {account_number}")
        return redirect('dps_search')

@login_required
@permission_required('app1.add_dps', raise_exception=True)
def dps_list(request):

    data = DPS.objects.filter().order_by('-id')
    for dps in data:
        dps.due_amount = dps.total_amount - dps.balance

    return render(request, 'app1/dps/dps_list.html', {'data': data})

@login_required
def dps_schedule(request, id):
    dps = DPS.objects.get(id=id)
    schedules = dps.dps_installment_schedules.all()
    paid_installments_count = schedules.filter(installment_status='paid').count()
    holidays = Holiday.objects.values_list('date', flat=True)
    due = dps.total_amount - dps.balance
    context = {
        'dps': dps,
        'schedules': schedules,
        'holidays': holidays,
        'paid_installments_count': paid_installments_count,
        'due': due,
    }
    return render(request, 'app1/dps/dps_schedule.html', context)

@login_required
@permission_required('app1.add_dps', raise_exception=True)
def dps_transaction(request, id):
    dps = DPS.objects.get(id=id)
    transactions = dps.dps_transaction_history.all().order_by('-date')
    return render(request, 'app1/dps/dps_transaction.html', {'dps': dps, 'transactions': transactions})

@login_required
def dps_deposit(request, id):
    dps = get_object_or_404(DPS, id=id)

    if request.method == "POST":
        form = DPSTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = dps
            transaction.transaction_type = "deposit"

            # Update DPS balance
            dps.total_deposit += transaction.amount
            dps.balance += transaction.amount
            dps.save()
            transaction.save()

            # Calculate how many installments can be paid
            amount_per_installment = dps.amount_per_installments
            num_to_pay = int(dps.balance / amount_per_installment)

            installments = dps.dps_installment_schedules.filter().order_by('due_date')[:num_to_pay]

            for installment in installments:
                installment.installment_status = 'paid'
                installment.save()
                
            # Send SMS notification
            sms_msg = send_sms(
                number=dps.customer.customer_mobile,
                title='Deposit DPS AC',
                user=request.user,
                amount=transaction.amount,
                balance=dps.balance,
                dps_number=dps.customer.account_number,
            )

            messages.success(request, f"Deposit of {transaction.amount} was successful and installments were processed!")
            return redirect('dps_deposit', id=id)
    else:
        form = DPSTransactionForm()

    context = {
        'form': form,
        'dps': dps,
        'transaction_type': 'Deposit',
    }
    return render(request, 'app1/dps/dps_dw.html', context)

@login_required
def dps_withdraw(request, id):
    dps = get_object_or_404(DPS, id=id)

    if request.method == "POST":
        form = DPSTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = dps
            transaction.transaction_type = "withdraw"
            withdraw_amount = transaction.amount
            if transaction.amount > dps.balance:
                messages.error(request, "Insufficient balance for withdrawal.")
                return redirect('dps_withdraw', id=id)

            # Update account balance
            dps.total_withdraw += transaction.amount
            dps.balance -= transaction.amount
            dps.save()
            transaction.save()
            
            amount_per_installment = dps.amount_per_installments
            num_to_pay = int(dps.balance / amount_per_installment)

            # Get unpaid installments
            installments = dps.dps_installment_schedules.filter().order_by('due_date')
            due_installments = installments[num_to_pay:]

            for installment in due_installments:
                installment.installment_status = 'due'
                installment.save()
                

            # Send SMS notification
            sms_msg = send_sms(
                number=dps.customer.customer_mobile,
                title='Withdraw DPS AC',
                user=request.user,
                amount=transaction.amount,
                balance=dps.balance,
                account_number=dps.customer.account_number,
            )

            messages.success(request, f"Withdrawal of {withdraw_amount} was successful!")
            return redirect('dps_withdraw', id=id)
    else:
        form = DPSTransactionForm()

    context = {
        'form': form,
        'dps': dps,
        'transaction_type': 'Withdraw',
    }
    return render(request, 'app1/dps/dps_dw.html', context)

@login_required
@permission_required('app1.add_dps', raise_exception=True)
def dps_close_search(request):
 
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        
        # Check if the customer exists in the active branch
        customer = Customer.objects.filter(account_number=account_number).first()
        
        if customer:
           
            dps = DPS.objects.filter(customer=customer)
            
            if dps.exists():
                return render(request, 'app1/dps/dps_cs_results.html', {'dps': dps, 'customer': customer})
            else:
                return render(request, 'app1/dps/dps_cs.html', {'error': 'No loans found for this account number.'})
        else:
            return render(request, 'app1/dps/dps_cs.html', {'error': 'No customer found with this account number in the current branch.'})
    return render(request, 'app1/dps/dps_cs.html')

@login_required
@require_POST
@permission_required('app1.add_dps', raise_exception=True)
def dps_close(request, id):
    dps = get_object_or_404(DPS, id=id)
    
    # Retrieve values from POST request
    profit_percentage = request.POST.get('profit_percentage')
    profit_taka = request.POST.get('profit_taka')
    closing_charge = request.POST.get('closing_charge')
    bonus = request.POST.get('performance_bonus')
    
    # Convert values to float and update the model
    if profit_percentage:
        dps.profit_percent = float(profit_percentage)
    if profit_taka:
        dps.profit_taka = float(profit_taka)
    if closing_charge:
        dps.dps_closing_charge = float(closing_charge)
    if bonus:
        dps.bonus = float(bonus)

    # Update status and save the model
    dps.status = 'closed'
    dps.save(update_fields=['status', 'profit_percent', 'profit_taka', 'dps_closing_charge', 'bonus'])

    sms_msg = send_sms(
        number=dps.customer.mobile_number,
        title='DPS Closing',
        user=request.user,
        account_number=dps.customer.account_number,
    )
    messages.success(request, sms_msg)
    UserLog.objects.create(processed_by=request.user,logs_action='DPS AC Closed',description=f'Account Number: {dps.customer.account_number}, DPS ID: {dps.transaction_id}')

    UserLog.objects.create(processed_by=request.user,action=f'DPS Closing',amount=dps.balance, customer=dps.customer, trx=True)
    UserLog.objects.create(processed_by=request.user,action=f'DPS Profit Withdraw',amount=profit_taka, customer=dps.customer, trx=True)
    UserLog.objects.create(processed_by=request.user,action=f'DPS Performance Bonus',amount=bonus, customer=dps.customer, trx=True)
    UserLog.objects.create(processed_by=request.user,action=f'DPS Closing Charge',amount=closing_charge, customer=dps.customer)
    return redirect('dps_list')

# DPS
################################################################

################################################################
# ShareAC

@login_required
@permission_required('app1.view_shareac', raise_exception=True)
def share_list(request):
   
    customers = ShareAC.objects.filter()
    return render(request, 'app1/share/share_list.html', {'customers': customers})

@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_create(request, account_number):
    try:
        print(account_number)
        customer = Customer.objects.get(account_number=account_number)

        if request.method == 'POST':
            balance = request.POST.get('balance')
            nominee = request.POST.get('nominee')
            note = request.POST.get('note')

            share = ShareAC(
                customer=customer,
                balance=balance,
                nominee=nominee,
                deposit=balance,
            )
            share.save()

            messages.success(request, f"Share Account created successfully.")

            trx = ShareACTransactionHistory.objects.create(
                account=share,
                transaction_type='deposit',
                amount=Decimal(balance),
                # processed_by=request.user,
                note=note,
                # balance=share.balance,
            )

            sms_msg = send_sms(
                number=customer.customer_mobile,
                title='Add Share AC',
                user=request.user,
            )
            messages.success(request, sms_msg)
            # UserLog.objects.create(processed_by=request.user,logs_action='Add Share AC',description=f'Account Number: {customer.account_number}')
            # UserLog.objects.create(processed_by=request.user,action=f'Share AC Previous Balance',amount=balance, customer=customer)
            return redirect('share_list')

        context = {'customer': customer}
        return render(request, 'app1/share/share_create.html', context)
    
    except Customer.DoesNotExist:
        messages.error(request, f"No customer found with account number: {account_number}")
        return redirect('share_search')

@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_deposit(request, share_id):
    share_ac = get_object_or_404(ShareAC, share_id=share_id)
    customer = share_ac.customer

    if request.method == "POST":
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = share_ac
            transaction.transaction_type = "deposit"

            share_ac.balance += transaction.amount
            share_ac.deposit += transaction.amount
            share_ac.save()
            transaction.save()

            sms_msg = send_sms(
                number=customer.customer_mobile,
                title='Deposit Share AC',
                user=request.user,
                amount=transaction.amount,
                balance=share_ac.balance,
                account_number=customer.account_number,
            )

            messages.success(request, f"Deposit of {transaction.amount} was successful!")
            return redirect('share_deposit', share_id=share_id)
    else:
        form = ShareTransactionForm()

    return render(request, 'app1/share/share_dw.html', {'form': form, 'share_ac': share_ac, 'transaction_type': 'Deposit'})

@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_withdraw(request, share_id):
    share_ac = get_object_or_404(ShareAC, share_id=share_id)
    customer = share_ac.customer

    if request.method == "POST":
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = share_ac
            transaction.transaction_type = "withdraw"

            if transaction.amount > share_ac.balance:
                messages.error(request, "Insufficient balance for withdrawal.")
                return redirect('share_withdraw', share_id=share_id)

            share_ac.balance -= transaction.amount
            share_ac.withdraw += transaction.amount
            share_ac.save()
            transaction.save()

            sms_msg = send_sms(
                number=customer.customer_mobile,
                title='Withdraw Share AC',
                user=request.user,
                amount=transaction.amount,
                balance=share_ac.balance,
                account_number=customer.account_number,
            )
       

            UserLog.objects.create(
                processed_by=request.user,
                logs_action='Withdraw Share AC',
                description=f'Account Number: {customer.account_number}, TrxID: {transaction.VoucherID}'
            )
            messages.success(request, f"Withdraw of {transaction.amount} was successful!")
            return redirect('share_withdraw', share_id=share_id)

    else:
        form = ShareTransactionForm()

    return render(request, 'app1/share/share_dw.html', {'form': form, 'share_ac': share_ac, 'transaction_type': 'Withdraw'})



@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_profit_withdraw(request, share_id):
    share_ac = get_object_or_404(ShareAC, share_id=share_id)
    customer = share_ac.customer

    if request.method == 'POST':
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        note = f'{note} Profit Withdraw'
        processed_by = request.user

        # share_ac.balance -= Decimal(amount)
        share_ac.profit_withdraw += Decimal(amount)
        share_ac.save()

        share_trx = ShareACTransactionHistory.objects.create(
            share_ac=share_ac,
            transaction_type='withdraw',
            Amount=Decimal(amount),
            processed_by=processed_by,
            note=note,
            balance=share_ac.balance,
        )
        sms_msg = send_sms(
            number=share_ac.customer.mobile_number,
            title='Profit Withdraw Share AC',
            user=request.user,
            amount=amount,
            balance=share_ac.profit_balance,
            account_number=share_ac.customer.account_number,
        )
        messages.success(request, sms_msg)
        UserLog.objects.create(processed_by=request.user,logs_action='Profit Withdraw Share AC',description=f'Account Number: {customer.account_number}, TrxID: {share_trx.VoucherID}')
        UserLog.objects.create(processed_by=request.user,action=f'Profit Withdraw Share AC',amount=amount, customer=customer, trx=True)

        return redirect('share_list')

    return render(request, 'app1/share/share_profit_withdraw.html', {'share_ac': share_ac, 'customer': customer})

@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_transfer(request, share_id):
    share_ac = get_object_or_404(ShareAC, share_id=share_id)
    customer = share_ac.customer
    prev_customer = customer
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        nominee = request.POST.get('nominee')
        customer = get_object_or_404(Customer, account_number=account_number)

        share_ac.customer = customer
        share_ac.nominee = nominee
        share_ac.save()

        UserLog.objects.create(processed_by=request.user,logs_action='Transfer Share AC',description=f'Share ID: {share_ac.share_id}, From:{prev_customer.account_number}, To: {share_ac.customer.account_number}')

        return redirect('share_list')

    return render(request, 'app1/share/share_transfer.html', {'share_ac': share_ac, 'customer': customer})

@login_required
@permission_required('app1.view_shareactransactionhistory', raise_exception=True)
def share_transaction_history(request, share_id):
    share_ac = ShareAC.objects.get(share_id=share_id)
    transactions = share_ac.share_ac_transaction_history.all().order_by('-id')
    return render(request, 'app1/share/share_transactions.html', {'data': share_ac, 'transactions': transactions})

@login_required
@permission_required('app1.view_shareac', raise_exception=True)
def share_search(request):
    return render(request, 'app1/share/share_search.html')

@login_required
@permission_required('app1.add_shareac', raise_exception=True)
def share_profit_withdraw_search(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        try:
            share_ac = ShareAC.objects.get(customer__account_number=account_number)
            return redirect('share_profit_withdraw', share_ac.share_id)
        except ShareAC.DoesNotExist:
            context = {'error': f'No share account found with account number: {account_number}'}
            return render(request, 'app1/share/share_deposit_search.html', context)
    return render(request, 'app1/share/share_deposit_search.html')

# ShareAC
################################################################

from django.db import transaction as db_transaction

@login_required
@permission_required('app1.add_banktransaction', raise_exception=True)
def bank_transaction_view(request):
    if request.method == 'POST':
        form = BankTransactionForm(request.POST, request.FILES)
        if form.is_valid():
            with db_transaction.atomic():
                transaction_instance = form.save(commit=False)
                bank = transaction_instance.bank

                if transaction_instance.transaction_type == 'deposit':
                    bank.balance += transaction_instance.amount
                elif transaction_instance.transaction_type == 'withdraw':
                    if transaction_instance.amount > bank.balance:
                        messages.error(request, "Insufficient balance for withdrawal.")
                        return redirect('bank_transaction_view')
                    bank.balance -= transaction_instance.amount

                # Save updated bank balance and transaction
                bank.save()
                transaction_instance.save()

            return redirect('bank_transaction_view')
    else:
        form = BankTransactionForm()

    transactions = BankTransaction.objects.select_related('bank').order_by('-id')
    
    return render(request, 'app1/others/bank_transaction.html', {
        'form': form,
        'transactions': transactions
    })

@login_required
def voucher_transaction_view(request):
    if request.method == "POST":
        form = VoucherTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('voucher_transaction_view')
    else:
        form = VoucherTransactionForm()
        
    transactions = VoucherTransaction.objects.select_related('voucher').order_by('-date')
    return render(request, 'app1/others/voucher_transaction.html', {'form': form, 'transactions': transactions})


################################################################
# Delete

@login_required
@permission_required('app1.delete_customer', raise_exception=True)
def delete_search(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        print(account_number)
        customer = Customer.objects.filter(account_number=account_number).first()
        if customer:
            dps = DPS.objects.filter(customer=customer)
            share = ShareAC.objects.filter(customer=customer)
            general = GeneralAC.objects.filter(customer=customer).first()
            savings = SavingsAC.objects.filter(customer=customer).first()
            
            context={
                'dpss': dps,
                'shares': share,
                'general': general,
                'savings': savings,
                'customer': customer,
            }
            return render(request, 'app1/others/delete_search_results.html', context)

        else:
            return render(request, 'app1/others/delete_search.html', {'error': 'No customer found with this account number in the current branch.'})
    return render(request, 'app1/others/delete_search.html')

@login_required
@permission_required('app1.delete_customer', raise_exception=True)
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customer_list')

@login_required
@permission_required('app1.delete_dps', raise_exception=True)
def dps_delete(request, id):
    dps = get_object_or_404(DPS, id=id)
    dps.delete()
    return redirect('delete_search')

@login_required
@permission_required('app1.delete_shareac', raise_exception=True)
def share_delete(request, share_id):
    share = get_object_or_404(ShareAC, share_id=share_id)
    share.delete()
    return redirect('delete_search')

# Delete
################################################################

@login_required
def set_language(request):
    language = request.POST.get('language', 'en')
    request.session['language'] = language
    return redirect('/')



