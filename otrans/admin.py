from django.contrib import admin
from .models import Expense, GetOutLoan, Income, Deposit, Withdraw, Passbook

# @admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('voucher_category', 'CustomerName', 'Amount', 'ExpenseDate', 'VoucherID')

# @admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('voucher_category', 'CustomerName', 'Amount', 'IncomeDate', 'VoucherID')

# @admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ( 'Amount', 'Date', 'VoucherID')

# @admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):  # Fixed class name capitalization
    list_display = ( 'Amount', 'Date', 'VoucherID')

# @admin.register(Passbook)
class PassbookAdmin(admin.ModelAdmin):  # Fixed class name capitalization
    list_display = ( 'Account', 'Amount', 'Date')

# @admin.register(GetOutLoan)
class GetOutLoanAdmin(admin.ModelAdmin):
    list_display = ( 'current_amount', 'date', 'VoucherID')
    
