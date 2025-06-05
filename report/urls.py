from django.urls import path
from . import views

urlpatterns = [
    path('customer-balance/', views.customer_balance, name='customer_balance'),
    path('customer-statement/', views.customer_statement, name='account_statement'),
    
    path('admission-report/', views.admission_report, name='customer_report'),
    path('dps_report/', views.dps_report, name='dps_report'),
    path('share_report/', views.share_report, name='share_report'),
    
    path('general_ledger/', views.general_ledger, name='general_ledger'),
    path('bank-transactions/', views.bank_transactions, name='bank_transactions'),
    
    path('monthly_top_sheet_report/', views.monthly_top_sheet_report, name='monthly_top_sheet_report'),
    path('yearly_top_sheet_report/', views.yearly_top_sheet_report, name='yearly_top_sheet_report'),


    path('voucher_report/', views.voucher_report, name='voucher_report'),
    
    
    # path('balance_sheet/', views.balance_sheet, name='balance_sheet'),
    # path('user_log/', views.user_log, name='user_log'),
    # path('user_entry_summary/', views.user_entry_summary, name='user_entry_summary'),
    # path('user_wise_entry_summary/', views.user_wise_entry_summary, name='user_wise_entry_summary'),
    # path('ReceivePayment/', views.ReceivePayment, name='ReceivePayment'),
    # path('ProfitLoss/', views.ProfitLoss, name='ProfitLoss'),
]





