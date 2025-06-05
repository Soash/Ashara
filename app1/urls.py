from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('home/', views.home, name='home'),
    path('customer_home/', views.customer_home, name='customer_home'),
    path('set_language/', views.set_language, name='set_language'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-logout/', views.customer_signout, name='customer_logout'),
    path('customer_change_password/', views.customer_change_password, name='customer_change_password'),
    path('access-denied/', views.access_denied, name='access_denied'),

    path('manage-permissions/', views.manage_permissions, name='manage_permissions'),

    path('customers-add/', views.customer_add, name='customer_add'),
    path('customers-list/', views.customer_list, name='customer_list'),
    path('customers-details/<int:id>/', views.customer_details, name='customer_details'),
    path('customers-edit/<int:id>/', views.customer_edit, name='customer_edit'),

    path('general-list/', views.general_list, name='general_list'),
    path('general-deposit/<int:id>/', views.general_deposit, name='general_deposit'),
    path('general-withdraw/<int:id>/', views.general_withdraw, name='general_withdraw'),
    path('general-transactions/<int:id>/', views.general_transaction_history, name='general_transaction_history'),
    # path('general-deposit-search/', views.general_deposit_search, name='general_deposit_search'),
    # path('general-withdraw-search/', views.general_withdraw_search, name='general_withdraw_search'),

    path('savings-list/', views.savings_list, name='savings_list'),
    path('savings-deposit/<int:id>/', views.savings_deposit, name='savings_deposit'),
    path('savings-withdraw/<int:id>/', views.savings_withdraw, name='savings_withdraw'),
    path('savings-transactions/<int:id>/', views.savings_transaction_history, name='savings_transaction_history'),
    # path('savings-deposit-search/', views.savings_deposit_search, name='savings_deposit_search'),
    # path('savings-withdraw-search/', views.savings_withdraw_search, name='savings_withdraw_search'),





    path('dps-search/', views.dps_search, name='dps_search'),
    path('dps-list/', views.dps_list, name='dps_list'),
    path('dps-create/<str:account_number>/', views.dps_create, name='dps_create'),
    path('dps-schedule/<int:id>/', views.dps_schedule, name='dps_schedule'),
    path('dps-deposit/<int:id>/', views.dps_deposit, name='dps_deposit'),
    path('dps-withdraw/<int:id>/', views.dps_withdraw, name='dps_withdraw'),
    path('dps-transaction/<int:id>/', views.dps_transaction, name='dps_transaction'),
    # path('dps-deposit-search/', views.dps_deposit_search, name='dps_deposit_search'),
    # path('dps-withdraw-search/', views.dps_withdraw_search, name='dps_withdraw_search'),
    path('dps-close-search/', views.dps_close_search, name='dps_close_search'),
    path('dps-close/<int:id>/', views.dps_close, name='dps_close'),



    path('share-list/', views.share_list, name='share_list'),
    path('share-create/<str:account_number>/', views.share_create, name='share_create'),
    path('share-search/', views.share_search, name='share_search'),
    path('share-deposit/<int:share_id>/', views.share_deposit, name='share_deposit'),
    # path('share-deposit-search/', views.share_deposit_search, name='share_deposit_search'),
    # path('share-withdraw-search/', views.share_withdraw_search, name='share_withdraw_search'),
    path('share-profit-withdraw-search/', views.share_profit_withdraw_search, name='share_profit_withdraw_search'),
    path('share-withdraw/<int:share_id>/', views.share_withdraw, name='share_withdraw'),
    path('share-transfer/<int:share_id>/', views.share_transfer, name='share_transfer'),
    path('share-profit-withdraw/<int:share_id>/', views.share_profit_withdraw, name='share_profit_withdraw'),
    path('share-transaction-history/<int:share_id>/', views.share_transaction_history, name='share_transaction_history'),

    # path('bank_withdraw/', views.bank_withdraw, name='bank_withdraw'),
    # path('bank_deposit/', views.bank_deposit, name='bank_deposit'),
    
    path('bank-transactions/', views.bank_transaction_view, name='bank_transaction_view'),
    path('voucher-transactions/', views.voucher_transaction_view, name='voucher_transaction_view'),
    
    path('package/', views.package, name='package'),
    path('delete-search/', views.delete_search, name='delete_search'),
    path('delete-customer/<int:id>/', views.delete_customer, name='delete_customer'),
    path('delete-dps/<int:id>/', views.dps_delete, name='dps_delete'),
    path('delete-share/<int:share_id>/', views.share_delete, name='share_delete'),
]


