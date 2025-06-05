from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from app1.models import DPS, DPSTransactionHistory, GeneralAC, GeneralTransactionHistory, Customer, SavingsAC, SavingsTransactionHistory, ShareAC, ShareACTransactionHistory
from otrans.models import Expense, Income
from report.models import UserLog
from .forms import AccountStatementForm, DPSReportForm, GeneralLedgerForm, CustomerSearchForm, ProfitLossReportForm, ReceivePaymentReportForm, ReportForm, ShareReportForm, UESReportForm, UWESReportForm, VoucherReportForm, YearlyTopSheetForm
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Sum, F, Q, ExpressionWrapper, DecimalField, Value, CharField
from primary_setup.models import Bank, CustomUser, Director, OutLoan, BankTransaction, VoucherTransaction
from datetime import datetime
from datetime import datetime
from django.db.models import Sum
from .forms import GeneralLedgerForm
from app1.models import ShareACTransactionHistory, DPSTransactionHistory, SavingsTransactionHistory, GeneralTransactionHistory



@login_required
def customer_statement(request):
    
    if request.method == 'POST':
        form = AccountStatementForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            account_number = form.cleaned_data['account_number']

            customer = Customer.objects.get(account_number=account_number)
            
            # Try to retrieve associated accounts, avoid errors if not found
            try:
                general = GeneralAC.objects.get(customer=customer)
            except GeneralAC.DoesNotExist:
                general = None

            try:
                savings = SavingsAC.objects.get(customer=customer)
            except SavingsAC.DoesNotExist:
                savings = None

            try:
                share = ShareAC.objects.get(customer=customer)
            except ShareAC.DoesNotExist:
                share = None

            try:
                dps = DPS.objects.get(customer=customer)
            except DPS.DoesNotExist:
                dps = None
            
            if end_date:
                end_date = end_date + timedelta(days=1)
                
            date_filter = {}
            if start_date and end_date:
                date_filter = {'date__range': (start_date, end_date)}




            # Filter transactions based on the date range or return all transactions if no dates are provided
            general_trans = GeneralTransactionHistory.objects.filter(account__customer=customer, **date_filter)
            special_trans = SavingsTransactionHistory.objects.filter(account__customer=customer, **date_filter)
            share_trans = ShareACTransactionHistory.objects.filter(account__customer=customer, **date_filter)
            dps_trans = DPSTransactionHistory.objects.filter(account__customer=customer, **date_filter)



            date_filter = {}
            if start_date and end_date:
                date_filter = {'date__range': (start_date, end_date)} 



            # Summing up deposits and withdrawals
            general_deposit_sum = general_trans.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
            general_withdraw_sum = general_trans.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0

            special_deposit_sum = special_trans.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
            special_withdraw_sum = special_trans.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0

            share_deposit_sum = share_trans.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
            share_withdraw_sum = share_trans.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0



            dps_deposit_sum = dps_trans.filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
            dps_withdraw_sum = dps_trans.filter(transaction_type='withdraw').aggregate(Sum('amount'))['amount__sum'] or 0


            total_deposit_sum = general_deposit_sum + special_deposit_sum + share_deposit_sum + dps_deposit_sum
            total_withdraw_sum = general_withdraw_sum + special_withdraw_sum + share_withdraw_sum + dps_withdraw_sum
            
            total_current_balance = total_deposit_sum - total_withdraw_sum
            total_current_balance = round(total_current_balance, 2)

            context = {
                'general_trans': general_trans,
                'savings_trans': special_trans,
                'share_ac_trans': share_trans,
                'dps_transaction_history': dps_trans,
                'customer': customer,
                'general_deposit_sum': general_deposit_sum,
                'general_withdraw_sum': general_withdraw_sum,
                'special_deposit_sum': special_deposit_sum,
                'special_withdraw_sum': special_withdraw_sum,
                'share_deposit_sum': share_deposit_sum,
                'share_withdraw_sum': share_withdraw_sum,
                'dps_deposit_sum': dps_deposit_sum,
                'dps_withdraw_sum': dps_withdraw_sum,
                'total_deposit_sum': total_deposit_sum,
                'total_withdraw_sum': total_withdraw_sum,
                'total_current_balance': total_current_balance,
                
                'general': general,
                'savings': savings,
                'share': share,
                'dps': dps,
            }

            return render(request, 'report/account_statment_print.html', context)
    else:
        form = AccountStatementForm()

    return render(request, 'report/account_statment.html', {'form': form})

@login_required
def admission_report(request):
    form = CustomerSearchForm()
    customers = []
    start_date = end_date = None
    if request.method == 'POST':
        form = CustomerSearchForm(request.POST, )
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            customers = Customer.objects.filter(
                joining_date__range=[start_date, end_date],
            )

    return render(request, 'report/customer_report.html', {
        'form': form,
        'customers': customers,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def customer_balance(request):
    

    if request.method == 'POST':
        account_no = request.POST.get('account_no')
        
        customer = Customer.objects.filter(account_number=account_no, ).first()

        if customer:
            # Fetch related accounts

            dps = DPS.objects.filter(customer=customer)

            share = ShareAC.objects.filter(customer=customer)
            generalAC = get_object_or_404(GeneralAC, customer=customer)
            savingsAC = get_object_or_404(SavingsAC, customer=customer)

            # Calculate balances

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
                'special_savings': special_savings
            }
            return render(request, 'report/customer_balance.html', context)

        else:
            return render(request, 'report/search.html', {'error': 'No customer found with this account number in the current branch.'})

    return render(request, 'report/search.html')

@login_required
def bank_transactions(request):
    banks = Bank.objects.all()
    bank = None
    total_deposit = 0
    total_withdraw = 0
    transactions = []
    total_balance = round(banks.aggregate(total=Sum('balance'))['total'] or 0, 2)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        bank_id = request.POST.get('bank')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'report/bank_transaction_report.html', {'error': 'Invalid date format'})

        if bank_id == 'all':
            transactions = BankTransaction.objects.filter(
                date__gte=start_date,
                date__lte=end_date,
            )
            total_balance = total_balance
        else:
            try:
                bank = Bank.objects.get(id=bank_id)
                transactions = BankTransaction.objects.filter(
                    date__gte=start_date,
                    date__lte=end_date,
                    bank=bank
                )
                total_balance = bank.balance
            except Bank.DoesNotExist:
                return render(request, 'report/bank_transaction_report.html', {'error': 'Invalid bank selection'})

        # Calculate totals
        total_deposit = transactions.filter(transaction_type='deposit').aggregate(total=Sum('amount'))['total'] or 0
        total_withdraw = transactions.filter(transaction_type='withdraw').aggregate(total=Sum('amount'))['total'] or 0
        net_balance = total_deposit - total_withdraw
        return render(request, 'report/bank_transaction_report.html', {
            'transactions': transactions,
            'banks': banks,
            'bank': bank,
            # 'report_date': report_date,
            'start_date': start_date,
            'end_date': end_date,
            'total_deposit': total_deposit,
            'total_withdraw': total_withdraw,
            'total_balance': total_balance,
            'net_balance': net_balance
        })

    return render(request, 'report/bank_transaction_report.html', {
        'banks': banks,
        'start_date': None,
        'end_date': None,
        'total_balance': total_balance
    })






@login_required
def voucher_report(request):
    entries = None
    totals = {'total_amount': 0}

    if request.method == 'POST':
        form = VoucherReportForm(request.POST)
        if form.is_valid():
            voucher_category = form.cleaned_data.get('voucher_category')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            entries = VoucherTransaction.objects.all()

            if voucher_category:
                entries = entries.filter(voucher=voucher_category)

            if start_date and end_date:
                entries = entries.filter(date__range=(start_date, end_date))

            totals = entries.aggregate(total_amount=Sum('amount'))
            
            if voucher_category == None:
                voucher_category = 'All'
            return render(request, 'report/voucher_print.html', {
                'entries': entries,
                'totals': totals,
                'form': form,
                'start_date': start_date,
                'end_date': end_date,
                'voucher_category': voucher_category
            })
    else:
        form = VoucherReportForm()

    return render(request, 'report/voucher.html', {
        'form': form,
        'entries': entries,
        'totals': totals,
    })





@login_required
def balance_sheet(request):
    
    today = date.today()



  
    cash_in_bank = Bank.objects.filter().aggregate(total_loan=Sum('balance'))['total_loan'] or 0
    cash_in_hand = 0
    total_asset = (cash_in_bank + cash_in_hand)
    

    general_savings_daily = GeneralAC.objects.filter(customer__customer_type='daily').aggregate(total=Sum('balance'))['total'] or 0
    general_savings_weekly = GeneralAC.objects.filter(customer__customer_type='weekly').aggregate(total=Sum('balance'))['total'] or 0
    general_savings_monthly = GeneralAC.objects.filter(customer__customer_type='monthly').aggregate(total=Sum('balance'))['total'] or 0

    special_savings_daily = SavingsAC.objects.filter(customer__customer_type='daily').aggregate(total=Sum('balance'))['total'] or 0
    special_savings_weekly = SavingsAC.objects.filter(customer__customer_type='weekly').aggregate(total=Sum('balance'))['total'] or 0
    special_savings_monthly = SavingsAC.objects.filter(customer__customer_type='monthly').aggregate(total=Sum('balance'))['total'] or 0

    share_balance = ShareAC.objects.filter().aggregate(total=Sum('balance'))['total'] or 0
    share_profit_balance = ShareAC.objects.filter().aggregate(total=Sum('profit_balance'))['total'] or 0

    dps_balance = DPS.objects.filter().aggregate(total=Sum('total_amount'))['total'] or 0

    director_balance = Director.objects.filter().aggregate(total=Sum('balance'))['total'] or 0
    outloan_balance = OutLoan.objects.filter().aggregate(total=Sum('balance'))['total'] or 0
    staff_balance = CustomUser.objects.filter().aggregate(total=Sum('balance'))['total'] or 0

    logs = UserLog.objects.filter().exclude(action__isnull=True).exclude(action__exact='').order_by('-id')
    receive_logs = logs.filter(cashflow_type2='receive').values('action').annotate(total_amount=Sum('amount')).order_by('action')
    payment_logs = logs.filter(cashflow_type2='payment').values('action').annotate(total_amount=Sum('amount')).order_by('action')
    total_receive = receive_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    total_payment = payment_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00

    accumulated_profit_loss = total_receive - total_payment

    total_capital = (
        Decimal(general_savings_daily) + Decimal(general_savings_weekly) + Decimal(general_savings_monthly) +
        Decimal(special_savings_daily) + Decimal(special_savings_weekly) + Decimal(special_savings_monthly) +
        Decimal(share_balance) + Decimal(share_profit_balance) + Decimal(dps_balance) +
        Decimal(director_balance) + Decimal(outloan_balance) + Decimal(staff_balance) + Decimal(accumulated_profit_loss) 
    )

    
    context = {
        'today': today,
        'cash_in_hand': cash_in_hand,
        'cash_in_bank': cash_in_bank,
        'total_asset': total_asset,

        'general_savings_daily': general_savings_daily,
        'general_savings_weekly': general_savings_weekly,
        'general_savings_monthly': general_savings_monthly,
        'special_savings_daily': special_savings_daily,
        'special_savings_weekly': special_savings_weekly,
        'special_savings_monthly': special_savings_monthly,
        'share_balance': share_balance,
        'share_profit_balance': share_profit_balance,
        'dps_balance': dps_balance,
        'director_balance': director_balance,
        'outloan_balance': outloan_balance,
        'staff_balance': staff_balance,
        'accumulated_profit_loss': accumulated_profit_loss,
        'total_capital': total_capital,
    }
    return render(request, 'report/balance_sheet.html', context)

@login_required
def user_log(request):

    logs_actions = UserLog.objects.filter().exclude(logs_action__isnull=True).exclude(logs_action__exact='').order_by('-id')
    return render(request, 'report/user_log.html', {'logs_actions': logs_actions})

@login_required
def user_entry_summary(request):

    if request.method == 'POST':
        form = UESReportForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            staff = form.cleaned_data['staff']

            logs = UserLog.objects.filter().exclude(action__isnull=True).exclude(action__exact='').order_by('-id')

            if start_date and end_date:
                end_date = end_date + timedelta(days=1)
                logs = logs.filter(timestamp__gte=start_date, timestamp__lt=end_date)

            if staff:
                logs = logs.filter(processed_by=staff)

            total_cash_in = logs.filter(transaction_type='cash_in').aggregate(Sum('amount'))['amount__sum'] or 0.00
            total_cash_out = logs.filter(transaction_type='cash_out').aggregate(Sum('amount'))['amount__sum'] or 0.00

            

            context ={
                'total_cash_in': total_cash_in,
                'total_cash_out': total_cash_out,
                'logs': logs,
                'staff':staff, 'start_date':start_date, 
                'end_date':end_date
            }
            return render(request, 'report/ues_print.html', context)
    else:
        form = UESReportForm(user=request.user)

    return render(request, 'report/ues.html', {'form': form})

@login_required
def user_wise_entry_summary(request):
    if request.method == 'POST':
        form = UWESReportForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Get all users who have logs within the date range
            logs = UserLog.objects.filter().exclude(action__isnull=True).exclude(action__exact='')

            if start_date and end_date:
                end_date = end_date + timedelta(days=1)
                logs = logs.filter(timestamp__gte=start_date, timestamp__lt=end_date)
            
            users = CustomUser.objects.filter(id__in=logs.values('processed_by')).distinct()

            # Initialize dictionaries for totals
            staff_data = []
            grand_total_cash_in = 0
            grand_total_cash_out = 0

            for user in users:
                user_logs = logs.filter(processed_by=user)
                total_cash_in = user_logs.filter(transaction_type='cash_in').aggregate(Sum('amount'))['amount__sum'] or 0.00
                total_cash_out = user_logs.filter(transaction_type='cash_out').aggregate(Sum('amount'))['amount__sum'] or 0.00
                balance = Decimal(total_cash_in) - Decimal(total_cash_out)

                staff_data.append({
                    'staff': user,
                    'total_cash_in': total_cash_in,
                    'total_cash_out': total_cash_out,
                    'balance': balance
                })

                grand_total_cash_in += Decimal(total_cash_in)
                grand_total_cash_out += Decimal(total_cash_out)

            grand_balance = grand_total_cash_in - grand_total_cash_out
            

            context = {
                'staff_data': staff_data,
                'grand_total_cash_in': grand_total_cash_in,
                'grand_total_cash_out': grand_total_cash_out,
                'grand_balance': grand_balance,
           
                'start_date': start_date,
                'end_date': end_date
            }

            return render(request, 'report/uwes_print.html', context)
    else:
        form = UWESReportForm(user=request.user)

    return render(request, 'report/uwes.html', {'form': form})






def general_ledger(request):
    form = GeneralLedgerForm(request.GET or None)
    transactions = []

    total_deposit = 0
    total_withdraw = 0
    net_balance = 0

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        account_number = form.cleaned_data.get('account_number')

        # Base Q object for filtering by date
        date_filter = Q(date__range=[start_date, end_date])

        # Apply account number filter if provided
        if account_number:
            # Apply the account_number filter on the Customer model through ShareAC
            account_filter = Q(account__customer__account_number=account_number)
            date_filter &= account_filter

        # Fetch transactions with annotated source and amount
        share_transactions = ShareACTransactionHistory.objects.filter(date_filter).annotate(
            source=Value("Share Account", output_field=CharField())
        )

        dps_transactions = DPSTransactionHistory.objects.filter(date_filter).annotate(
            source=Value("DPS Account", output_field=CharField())
        )

        savings_transactions = SavingsTransactionHistory.objects.filter(date_filter).annotate(
            source=Value("Savings Account", output_field=CharField())
        )

        general_transactions = GeneralTransactionHistory.objects.filter(date_filter).annotate(
            source=Value("General Account", output_field=CharField())
        )
        
        bank_transactions = BankTransaction.objects.filter(date_filter).annotate(
            source=Value("Bank Account", output_field=CharField())
        )
        
        voucher_transactions = VoucherTransaction.objects.filter(date_filter).annotate(
            source=Value("Voucher", output_field=CharField())
        )

        # Combine transactions
        transactions = list(share_transactions) + list(dps_transactions) + list(savings_transactions) + list(general_transactions) + list(bank_transactions) + list(voucher_transactions)

        # Calculate totals
        total_deposit = sum(t.amount for t in transactions if t.asset_type == "debit")
        total_withdraw = sum(t.amount for t in transactions if t.asset_type == "credit")

        net_balance = total_deposit - total_withdraw
        
        # Sort transactions by date
        transactions.sort(key=lambda x: x.date if x.date else '')

    return render(request, 'report/general_ledger.html', {
        'form': form,
        'transactions': transactions,
        'total_deposit': total_deposit,
        'total_withdraw': total_withdraw,
        'net_balance': net_balance,
    })










import calendar

def monthly_top_sheet_report(request):

    # Handle form submission (POST request)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            selected_month = int(form.cleaned_data['month'])
            selected_year = int(form.cleaned_data['year'])
                # Get the number of days in the selected month and year
            days_in_month = calendar.monthrange(selected_year, selected_month)[1]  # Get number of days in the month
            dates = [f"{selected_year}-{selected_month:02d}-{day:02d}" for day in range(1, days_in_month + 1)]

            # Pass the form and list of dates to the template
            return render(request, 'report/monthly_top_sheet.html', {
                'form': form,
                'dates': dates,
                'selected_month': selected_month,
                'selected_year': selected_year,
            })
    else:
        form = ReportForm()
        
    return render(request, 'report/monthly_top_sheet.html', {'form': form,})




def yearly_top_sheet_report(request):

    if request.method == 'POST':
        form = YearlyTopSheetForm(request.POST)
        if form.is_valid():
            selected_year = int(form.cleaned_data['year'])

            months = [f"{month:02d}" for month in range(1, 13)]

            return render(request, 'report/yearly_top_sheet.html', {
                'form': form,
                'months': months,
                'selected_year': selected_year,
            })
    else:
        form = YearlyTopSheetForm()
        
    return render(request, 'report/yearly_top_sheet.html', {'form': form,})




@login_required
def dps_report(request):
    dpss = None
    total_amount_per_installments = total_total_amount = total_balance = 0
    total_profit_taka = total_due = 0

    if request.method == 'POST':
        # form = DPSReportForm(request.POST, user=request.user)
        form = DPSReportForm(request.POST)
        if form.is_valid():
            # Retrieve the filter criteria from the form
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            scheme_name = form.cleaned_data['scheme_name']
            status = form.cleaned_data['status']
            account_number = form.cleaned_data['account_number']

            # Filter the FDR model based on the criteria
            dpss = DPS.objects.all()


            if start_date and end_date:
                dpss = dpss.filter(created_date__gte=start_date, created_date__lte=end_date)

            if scheme_name:
                dpss = dpss.filter(dps_scheme__scheme_name=scheme_name)

            if status and status != 'all':
                dpss = dpss.filter(status=status)

            if account_number:
                dpss = dpss.filter(customer__account_number=account_number)

            totals = dpss.aggregate(
                total_amount_per_installments=Sum('amount_per_installments'),
                total_total_amount=Sum('total_amount'),
                total_balance=Sum('balance'),
                total_profit_taka=Sum('profit_taka'),
                total_due=Sum(
                    ExpressionWrapper(
                        F('total_amount') - F('balance'),
                        output_field=DecimalField()
                    )
                )
            )

           
            return render(request, 'report/dps_print.html', {'dpss': dpss, 'totals': totals})
    else:
        # form = DPSReportForm(user=request.user)
        form = DPSReportForm()

    return render(request, 'report/dps.html', {'form': form})

@login_required
def share_report(request):
    share_ac = None
    total_balance = total_profit_balance = 0
    if request.method == 'POST':
        form = ShareReportForm(request.POST)
        if form.is_valid():
            # Retrieve the filter criteria from the form
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            account_number = form.cleaned_data['account_number']

            share_ac = ShareAC.objects.all()


            # if start_date and end_date:
            #     share_ac = share_ac.filter(created_at__gte=start_date, created_at__lte=end_date)

            if account_number:
                share_ac = share_ac.filter(customer__account_number=account_number)

            totals = share_ac.aggregate(
                total_balance=Sum('balance'),
                total_profit_balance=Sum('profit_balance'),
            )

            return render(request, 'report/share_print.html', {'share_ac': share_ac, 'totals': totals})
    else:
        form = ShareReportForm()

    return render(request, 'report/share.html', {'form': form})































@login_required
def ReceivePayment(request):

    if request.method == 'POST':
        form = ReceivePaymentReportForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Initial queryset
            logs = UserLog.objects.filter().exclude(action__isnull=True).exclude(action__exact='').order_by('-id')

            # Apply date filters
            if start_date and end_date:
                end_date = end_date + timedelta(days=1)
                logs = logs.filter(timestamp__gte=start_date, timestamp__lt=end_date)

            # Aggregate by action for receive and payment
            receive_logs = logs.filter(cashflow_type2='receive').values('action').annotate(total_amount=Sum('amount')).order_by('action')
            payment_logs = logs.filter(cashflow_type2='payment').values('action').annotate(total_amount=Sum('amount')).order_by('action')

            # Calculate totals
            total_receive = receive_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
            total_payment = payment_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00

            total_payment = float(total_payment)
            total_receive = float(total_receive)

            context = {
                'total_receive': total_receive,
                'total_payment': total_payment,
                'receive_logs': receive_logs,
                'payment_logs': payment_logs,
                
                'start_date': start_date,
                'end_date': end_date - timedelta(days=1),
                'final_balance': total_receive - total_payment,
            }

            return render(request, 'report/ReceivePayment_print.html', context)
    else:
        form = ReceivePaymentReportForm(user=request.user)

    return render(request, 'report/ReceivePayment.html', {'form': form})


@login_required
def ProfitLoss(request):
    
    if request.method == 'POST':
        form = ProfitLossReportForm(request.POST, user=request.user)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Initial queryset
            logs = UserLog.objects.filter().exclude(action__isnull=True).exclude(action__exact='').order_by('-id')

            # Apply date filters
            if start_date and end_date:
                end_date = end_date + timedelta(days=1)
                logs = logs.filter(timestamp__gte=start_date, timestamp__lt=end_date)

            # Aggregate by action for receive and payment
            receive_logs = logs.filter(cashflow_type2='receive').values('action').annotate(total_amount=Sum('amount')).order_by('action')
            payment_logs = logs.filter(cashflow_type2='payment').values('action').annotate(total_amount=Sum('amount')).order_by('action')

            # Calculate totals
            total_receive = receive_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
            total_payment = payment_logs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00

            total_payment = float(total_payment)
            total_receive = float(total_receive)
            
            context = {
                'total_receive': total_receive,
                'total_payment': total_payment,
                'receive_logs': receive_logs,
                'payment_logs': payment_logs,
                
                'start_date': start_date,
                'end_date': end_date - timedelta(days=1),
                'final_balance': total_receive - total_payment,
            }

            return render(request, 'report/ProfitLoss_print.html', context)
    else:
        form = ProfitLossReportForm(user=request.user)

    return render(request, 'report/ProfitLoss.html', {'form': form})



