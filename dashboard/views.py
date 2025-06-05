from datetime import datetime, timedelta  

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, permission_required

from django.utils import timezone
from primary_setup.models import CustomUser, Director, OutLoan, VoucherCategory
from app1.models import DPS, Customer, DPSTransactionHistory, GeneralAC, GeneralTransactionHistory, SavingsAC, SavingsTransactionHistory, ShareAC, ShareACTransactionHistory
from django.shortcuts import redirect
from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from otrans.models import Expense, Income, SSM_Deposit


@login_required
@permission_required('app1.view_generalac')
def today_dashboard(request, start_date=None, end_date=None):

    today = timezone.now().date()

    if start_date is None or end_date is None:
        start_date = today
        end_date = today
        dashboard = _("Today")
        dashboard1 = "Today"
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        dashboard = _("Monthly")
        dashboard1 = "Monthly"


    transactions = GeneralTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    general_savings_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    general_savings_transaction = transactions.aggregate(Count('id'))['id__count'] or 0

    transactions = SavingsTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    speical_savings_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    special_savings_transaction = transactions.aggregate(Count('id'))['id__count'] or 0


    
    transactions = DPSTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    dps_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    dps_transaction = transactions.aggregate(Count('id'))['id__count'] or 0


    transactions = ShareACTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    share_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    share_transaction = transactions.aggregate(Count('id'))['id__count'] or 0

    transactions = GeneralTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='withdraw'
    )
    savings_withdraw_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    savings_withdraw_transaction = transactions.aggregate(Count('id'))['id__count'] or 0

    transactions = DPSTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='withdraw'
    )
    dps_withdraw_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    dps_withdraw_transaction = transactions.aggregate(Count('id'))['id__count'] or 0

    
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    formatted_end_date = end_date.strftime('%Y-%m-%d')

    context = {
        'general_savings_collection': general_savings_collection,
        'general_savings_transaction': general_savings_transaction,
        'speical_savings_collection': speical_savings_collection,
        'special_savings_transaction': special_savings_transaction,
  
        'dps_collection': dps_collection,
        'dps_transaction': dps_transaction,

        'share_collection': share_collection,
        'share_transaction': share_transaction,
        'savings_withdraw_collection': savings_withdraw_collection,
        'savings_withdraw_transaction': savings_withdraw_transaction,
        'dps_withdraw_collection': dps_withdraw_collection,
        'dps_withdraw_transaction': dps_withdraw_transaction,

        'start_date': formatted_start_date,
        'end_date': formatted_end_date,  
        'dashboard': dashboard,
        'dashboard1': dashboard1,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@permission_required('app1.view_generalac')
def monthly_dashboard(request):
    today = timezone.now().date()

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    print(start_date_str)

    if start_date_str and end_date_str:
        # Convert string to date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        # Default to the current month's start and end dates
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)

    # Convert dates to strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    print(start_date_str)

    return redirect('today_dashboard', start_date=start_date_str, end_date=end_date_str)


@login_required
@permission_required('app1.view_generaltransactionhistory')
def general_savings_collection(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
 
    transactions = GeneralTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    total_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_total_collection = f"{total_collection:.2f}"
    
    context = {
        'total_collection': formatted_total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
        'title': 'General AC Deposit',
    }
    return render(request, 'dashboard/general_savings_collection_print.html', context)

@login_required
@permission_required('app1.view_savingstransactionhistory')
def special_savings_collection(request):


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
 
    transactions = SavingsTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    total_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_total_collection = f"{total_collection:.2f}"
    
    context = {
        'total_collection': formatted_total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
       
        'title': 'Savings AC Deposit',
    }
    return render(request, 'dashboard/general_savings_collection_print.html', context)


@login_required
def dps_collection(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
 
    transactions = DPSTransactionHistory.objects.filter(
   
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    total_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    # total_fine = transactions.aggregate(Sum('fine'))['fine__sum'] or 0
    total_fine = 0
    formatted_total_collection = f"{total_collection:.2f}"
    
    context = {
        'total_collection': formatted_total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,

        'title': 'DPS Deposit',
        'total_fine': total_fine,
    }
    return render(request, 'dashboard/dps_collection_print.html', context)

@login_required
def dps_withdraw_collection(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    transactions = DPSTransactionHistory.objects.filter(
      
        date__date__range=(start_date, end_date),
        transaction_type='withdraw'
    )
    total_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    # total_fine = transactions.aggregate(Sum('fine'))['fine__sum'] or 0
    total_fine = 0
    formatted_total_collection = f"{total_collection:.2f}"
    
    context = {
        'total_collection': formatted_total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
 
        'title': 'DPS Withdraw',
        'total_fine': total_fine,
    }
    return render(request, 'dashboard/dps_collection_print.html', context)


@login_required
def share_collection(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
 
    transactions = ShareACTransactionHistory.objects.filter(
        date__date__range=(start_date, end_date),
        transaction_type='deposit'
    )
    total_collection = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_total_collection = f"{total_collection:.2f}"
    
    context = {
        'total_collection': formatted_total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
 
        'title': 'Share AC Deposit',
    }
    return render(request, 'dashboard/share_collection_print.html', context)

@login_required
def savings_withdraw_collection(request):


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
 
    transactions = GeneralTransactionHistory.objects.filter(

        created_at__date__range=(start_date, end_date),
        transaction_type='withdraw'
    )
    total_collection = transactions.aggregate(Sum('Amount'))['Amount__sum'] or 0
    
    context = {
        'total_collection': total_collection,
        'transactions': transactions,
        'start_date': start_date,
        'end_date': end_date,
  
        'title': 'Savings Withdrawal',
    }
    return render(request, 'dashboard/general_savings_collection_print.html', context)



@login_required
def dashboard(request):


    total_general_savings = GeneralAC.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0
    total_special_savings = SavingsAC.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0
    total_dps_balance = DPS.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0

    total_dps_profit = DPS.objects.filter().aggregate(Sum('profit_taka'))['profit_taka__sum'] or 0
    total_share_balance = ShareAC.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0
    total_share_profit = ShareAC.objects.filter().aggregate(Sum('profit_balance'))['profit_balance__sum'] or 0

    voucher_category_count = VoucherCategory.objects.filter().count()
    total_income_amount = Income.objects.filter().aggregate(Sum('Amount'))['Amount__sum'] or 0
    total_expense_amount = Expense.objects.filter().aggregate(Sum('Amount'))['Amount__sum'] or 0

    total_customers = Customer.objects.filter().count()
    daily_customers = Customer.objects.filter(customer_type='daily').count()
    weekly_customers = Customer.objects.filter(customer_type='weekly').count()
    monthly_customers = Customer.objects.filter(customer_type='monthly').count()
    male_customers = Customer.objects.filter(gender='Male').count()
    female_customers = Customer.objects.filter(gender='Female').count()
    inactive_customers = Customer.objects.filter(status='Inactive').count()

    total_staff = CustomUser.objects.filter().count()

    total_general_ac = GeneralAC.objects.filter().count()
    total_dps = DPS.objects.filter().count()


    total_director = Director.objects.filter().count()
    total_director_balance = Director.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0

    total_outloan = OutLoan.objects.filter().count()
    total_OutLoan_balance = OutLoan.objects.filter().aggregate(Sum('balance'))['balance__sum'] or 0
    total_ssm_amount = SSM_Deposit.objects.filter().aggregate(Sum('Amount'))['Amount__sum'] or 0

    context = {
        'total_general_savings': total_general_savings,
        'total_special_savings': total_special_savings,
        'total_dps_balance': total_dps_balance,
        'total_dps_profit': total_dps_profit,
        'total_share_balance': total_share_balance,
        'total_share_profit': total_share_profit,
        'voucher_category_count': voucher_category_count,
        'total_income_amount': total_income_amount,
        'total_expense_amount': total_expense_amount,
        'total_customers': total_customers,
        'daily_customers': daily_customers,
        'weekly_customers': weekly_customers,
        'monthly_customers': monthly_customers,
        'male_customers': male_customers,
        'female_customers': female_customers,
        'inactive_customers': inactive_customers,
        'total_staff': total_staff,
        'total_general_ac': total_general_ac,
        'total_dps': total_dps,
        'total_director': total_director,
        'total_director_balance': total_director_balance,
        'total_outloan': total_outloan,
        'total_OutLoan_balance': total_OutLoan_balance,
        'total_ssm_amount': total_ssm_amount,
    }

    return render(request, 'dashboard/dashboard_all.html', context)


