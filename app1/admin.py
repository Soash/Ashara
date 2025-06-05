from django.contrib import admin
from .models import GeneralTransactionHistory, DPS, DPSInstallmentSchedule, Logo, Package, Customer, SavingsTransactionHistory, ShareACTransactionHistory
from .models import GeneralAC, SavingsAC, ShareAC
from django.contrib import admin


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "account_number", "customer_name", "customer_mobile", "joining_date", "share_count"
    )
    search_fields = ("customer_name", "account_number", "customer_mobile", "customer_nid")


class GeneralACAdmin(admin.ModelAdmin):
    list_display = ('customer', 'customer__account_number', 'status')
    search_fields = ('customer__account_number',)
    


class ShareACAdmin(admin.ModelAdmin):
    list_display = ('customer', 'balance')

# class GeneralDepositAdmin(admin.ModelAdmin):
#     list_display = ('VoucherID', 'Amount', 'Note', 'general')
#     search_fields = ('VoucherID',)


# class GeneralWithdrawAdmin(admin.ModelAdmin):
#     list_display = ('VoucherID', 'Amount', 'Note', 'created_at', 'processed_by', 'general')
#     search_fields = ('VoucherID',)



class GeneralTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'VoucherID',)
    list_filter = ('transaction_type',)
    search_fields = ('account__id', 'VoucherID',)


@admin.register(SavingsAC)
class SavingsACAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'status')

@admin.register(SavingsTransactionHistory)
class SavingsTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'VoucherID',)
    list_filter = ('transaction_type',)
    search_fields = ('account__id', 'VoucherID',)
    
@admin.register(ShareACTransactionHistory)
class ShareACTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'VoucherID',)
    list_filter = ('transaction_type',)
    search_fields = ('account__id', 'VoucherID',)









class DPSAdmin(admin.ModelAdmin):

    list_display = ('customer', 'created_date', 'total_amount',)
    search_fields = ('customer__name', 'transaction_id')
    list_filter = ('created_date',)


class DPSInstallmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('dps', 'installment_number', 'amount', 'due_date', 'skipped_due_date', 'installment_status')
    list_editable = ('installment_status',)  




# @admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'status', 'start_date', 'expired_date', 'billing_cycle', 'package_name', 'limit_customer')
    search_fields = ('client_id', 'package_name')
    list_filter = ('status', 'billing_cycle')
    
@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'somity_name', 'uploaded_at')
    
    


admin.site.register(GeneralAC, GeneralACAdmin)
admin.site.register(ShareAC, ShareACAdmin)
admin.site.register(DPS, DPSAdmin)
admin.site.register(GeneralTransactionHistory, GeneralTransactionHistoryAdmin)


admin.site.register(DPSInstallmentSchedule, DPSInstallmentScheduleAdmin)

# admin.site.register(GeneralDeposit, GeneralDepositAdmin)
# admin.site.register(GeneralWithdraw, GeneralWithdrawAdmin)


