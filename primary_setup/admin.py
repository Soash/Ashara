from django.contrib import admin
from .models import Bank, BankTransaction, CustomUser, Holiday, Director, OutLoan, VoucherCategory, DPSScheme, VoucherTransaction
from django.contrib.auth.admin import UserAdmin
from .models import SMSSetting



@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('account_no', 'bank_name', 'balance')
    exclude = ('balance',)

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('VoucherID', 'bank', 'transaction_type', 'amount', 'date')

@admin.register(CustomUser)   
class CustomUserAdmin(UserAdmin):
    list_display = ('username',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date')
    ordering = ('date',)

@admin.register(VoucherCategory)
class VoucherCategoryAdmin(admin.ModelAdmin):
    list_display = ('voucher_name',)

@admin.register(VoucherTransaction)
class VoucherTransactionAdmin(admin.ModelAdmin):
    list_display = ('VoucherID', 'voucher', 'amount', 'date')


@admin.register(DPSScheme)
class DPSSchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_name', 'payment_sequence',)


@admin.register(SMSSetting)
class SMSSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'language', 'content_bengali')
    list_editable = ('status',)
    list_filter = ('status',)












# class CustomUserAdmin(UserAdmin):
#     list_display = ('username','balance')
#     list_filter = ()

#     fieldsets = (
#         (None, {'fields': ('username', 'password', 'is_active', 'is_staff', 'is_superuser')}),
#         ('Personal info', {'fields': (('first_name', 'national_id'), ('email', 'mobile'), ('father_name', 'mother_name'), 'address')}),
#         # ('Organization', {'fields': (('group', ), 'date_joined',)}),
#         ('Organization', {'fields': ((), 'date_joined',)}),
#         ('Allowances', {'fields': (('basic_salary', 'house_rent'), ('medical_allowance', 'travel_allowance'), ('mobile_allowance', 'internet_allowance'))}),
#         # ('Permissions', {'fields': ('user_permissions', 'groups')}),
#         ('Permissions', {'fields': ('groups',)}),
#     )

#     add_fieldsets = (
#         (None, {'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff')}),
#         ('Personal info', {'fields': (('first_name', 'national_id'), ('email', 'mobile'), ('father_name', 'mother_name'), 'address')}),
#         ('Organization', {'fields': ((), 'date_joined',)}),
#         ('Allowances', {'fields': (('basic_salary', 'house_rent'), ('medical_allowance', 'travel_allowance'), ('mobile_allowance', 'internet_allowance'))}),
#         # ('Permissions', {'fields': ('user_permissions', 'groups')}),
#         ('Permissions', {'fields': ('groups',)}),
#     )
    

class FDRSchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_name', 'scheme_type', 'duration', 'profit_percent', 'note')


class LoanCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'profit_rate', 'loan_duration', 'max_loan_amount')


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'director_name', 'designation', 'mobile_number', 'profession', 'email', 'balance', 'status')


class OutLoanAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'company_name', 'mobile_number', 'profession', 'balance', 'profit', 'status')