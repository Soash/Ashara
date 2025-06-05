from decimal import Decimal
from django import template
from django.db.models import Sum
from app1.models import GeneralTransactionHistory, SavingsTransactionHistory, DPSTransactionHistory, ShareACTransactionHistory
from datetime import datetime

from primary_setup.models import BankTransaction, VoucherTransaction

register = template.Library()

# @register.filter
# def calculate_percentage(paid_amount, profit_percent):
#     try:
#         x = (paid_amount * profit_percent) / 100
#         return round(x, 2)
#     except (TypeError, ZeroDivisionError):
#         return 0
    
# @register.filter
# def calculate_principal(paid_amount, profit_percent):
#     try:
#         x = paid_amount - ((paid_amount * profit_percent) / 100)
#         return round(x, 2)
#     except (TypeError, ZeroDivisionError):
#         return 0

# @register.filter(name='sum')
# def sum_list(value):
#     return sum(value)

# @register.filter
# def split(value, delimiter=' '):
#     print(delimiter)
#     return value.split(delimiter)

@register.filter(name='has_permission')
def has_permission(user, perm_name):
    return user.has_perm(perm_name)

@register.filter
def sum_amounts(transactions, transaction_type):
    total = 0
    for transaction in transactions:
        if transaction.transaction_type == transaction_type:
            total += transaction.amount
    return "{:.2f}".format(total)

# @register.filter
# def sum_loan(queryset, field_name):
#     total = Decimal('0.00')
#     for obj in queryset:
#         value = getattr(obj, field_name, None)
#         if value:
#             total += value
#     return total

@register.filter
def sum_amounts_dps(transactions, transaction_type):
    total = 0
    for transaction in transactions:
        if transaction.transaction_type == transaction_type:
            total += transaction.amount
    return "{:.2f}".format(total)






# Monthly Top Sheet Report

@register.simple_tag
def total_amount_on_date(date, account_type, asset_type):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    # Calculate the total deposit for the given date
    if account_type == 'general':
        total_deposit = GeneralTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']
    elif account_type == 'savings':
        total_deposit = SavingsTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']
    elif account_type == 'dps':
        total_deposit = DPSTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']
    elif account_type == 'share':
        total_deposit = ShareACTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']
    elif account_type == 'bank':
        total_deposit = BankTransaction.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']
    elif account_type == 'voucher':
        total_deposit = VoucherTransaction.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total']

    # Return 0 if no deposit is found for the date
    return total_deposit if total_deposit else 0

@register.simple_tag
def total_amount_on_month(month, year, account_type, asset_type):
    # Calculate the total deposit for the given month and year
    if account_type == 'general':
        total_deposit = GeneralTransactionHistory.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']
    elif account_type == 'savings':
        total_deposit = SavingsTransactionHistory.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']
    elif account_type == 'dps':
        total_deposit = DPSTransactionHistory.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']
    elif account_type == 'share':
        total_deposit = ShareACTransactionHistory.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']
    elif account_type == 'bank':
        total_deposit = BankTransaction.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']
    elif account_type == 'voucher':
        total_deposit = VoucherTransaction.objects.filter(asset_type=asset_type, date__year=year, date__month=month).aggregate(total=Sum('amount'))['total']

    # Return 0 if no deposit is found for the month
    return total_deposit if total_deposit else 0

@register.simple_tag
def grand_total_on_date(date, asset_type):
    # Convert the date string to a datetime object
    
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    
    total_deposit_general = GeneralTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_savings = SavingsTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_dps = DPSTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_share = ShareACTransactionHistory.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    total_bank = BankTransaction.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    total_voucher = VoucherTransaction.objects.filter(asset_type=asset_type,date__date=date_obj).aggregate(total=Sum('amount'))['total'] or 0
    grand_total = total_deposit_general + total_deposit_savings + total_deposit_dps + total_deposit_share + total_bank + total_voucher

    # Return 0 if no deposit is found for the date
    return grand_total if grand_total else 0

@register.simple_tag
def grand_total_on_month(month, year, asset_type):
    # Convert the date string to a datetime object
    
    total_deposit_general = GeneralTransactionHistory.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_savings = SavingsTransactionHistory.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_dps = DPSTransactionHistory.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_share = ShareACTransactionHistory.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    total_bank = BankTransaction.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    total_voucher = VoucherTransaction.objects.filter(asset_type=asset_type,date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    grand_total = total_deposit_general + total_deposit_savings + total_deposit_dps + total_deposit_share + total_bank + total_voucher

    # Return 0 if no deposit is found for the date
    return grand_total if grand_total else 0

@register.simple_tag
def split_date(date):
    return date.split('-')[-1]



# Yearly Top Sheet Report
@register.simple_tag
def split_month(month):
    month_number = int(month)
    month_name = datetime(1900, month_number, 1).strftime('%b')
    return month_name

@register.simple_tag
def total_amount_on_year(year, account_type, asset_type):
    # Calculate the total deposit for the given month and year
    if account_type == 'general':
        total_deposit = GeneralTransactionHistory.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    elif account_type == 'savings':
        total_deposit = SavingsTransactionHistory.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    elif account_type == 'dps':
        total_deposit = DPSTransactionHistory.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    elif account_type == 'share':
        total_deposit = ShareACTransactionHistory.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    elif account_type == 'bank':
        total_deposit = BankTransaction.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    elif account_type == 'voucher':
        total_deposit = VoucherTransaction.objects.filter(asset_type=asset_type, date__year=year,).aggregate(total=Sum('amount'))['total'] or 0

    # Return 0 if no deposit is found for the month
    return total_deposit if total_deposit else 0

@register.simple_tag
def grand_total_on_year(year, asset_type):
    # Convert the date string to a datetime object
    
    total_deposit_general = GeneralTransactionHistory.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_savings = SavingsTransactionHistory.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_dps = DPSTransactionHistory.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    total_deposit_share = ShareACTransactionHistory.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    total_bank = BankTransaction.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    total_voucher = VoucherTransaction.objects.filter(asset_type=asset_type,date__year=year,).aggregate(total=Sum('amount'))['total'] or 0
    grand_total = total_deposit_general + total_deposit_savings + total_deposit_dps + total_deposit_share + total_bank + total_voucher

    # Return 0 if no deposit is found for the date
    return grand_total if grand_total else 0



@register.simple_tag
def sub(value1, value2):
    x = value1 - value2
    return x if x else 0

