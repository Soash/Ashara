from django.contrib import admin
from .models import UserLog

class UserLogAdmin(admin.ModelAdmin):
    list_display = (
        'processed_by',
        'action',
        'logs_action',
        'customer', 
        'transaction_type', 
        'cashflow_type1', 
        'cashflow_type2', 
        'amount', 
        'timestamp', 
        'ip_address', 
        'description'
    )
    search_fields = ('action', 'customer__customer_name', 'description')

    

# admin.site.register(UserLog, UserLogAdmin)

