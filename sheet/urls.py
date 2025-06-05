from django.urls import path
from . import views

urlpatterns = [
    # path('collection_sheet_filter/', views.collection_sheet_filter, name='collection_sheet_filter'),
    path('collection_sheet_1/', views.collection_sheet_1, name='collection_sheet_1'),
    
    
    
    path('select-somity/', views.select_somity, name='select_somity'),
    path('collection_sheet_filter2/', views.collection_sheet_filter2, name='collection_sheet_filter2'),

    path('savings_collection_sheet/<int:somity_id>/', views.savings_collection_sheet, name='savings_collection_sheet'),

    path('collection_sheet_2/<int:somity_id>/', views.collection_sheet2, name='collection_sheet2'),
]

