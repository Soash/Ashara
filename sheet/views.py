from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app1.models import Customer












@login_required
def collection_sheet_1(request):
    if request.method == 'POST' or 1==1:
        selected_date = request.POST.get('date')
        
        print(selected_date)
        
        customers = Customer.objects.filter().order_by('account_number')
        context={
            'customers': customers,
            'date': selected_date,
        }
        return render(request, 'sheet/collection_sheet.html', context)
    
    return render(request, 'sheet/collection_sheet.html')


















@login_required
def select_somity(request):
    if request.method == 'POST':
        selected_somity = request.POST.get('somity')
        return redirect('savings_collection_sheet', selected_somity)
    return render(request, 'sheet/select_somity.html', {'somities': "xyz"})

@login_required
def savings_collection_sheet(request, somity_id):

    customers = Customer.objects.filter()
    context={
        'customers': customers,

    }
    return render(request, 'sheet/savings_collection_sheet.html', context)











@login_required
def collection_sheet_filter2(request):

    if request.method == 'POST':
        selected_somity = request.POST.get('somity')
        return redirect('collection_sheet2', selected_somity)
    return render(request, 'sheet/select_somity.html', {'somities': "xyz"})

@login_required
def collection_sheet2(request, somity_id):
    customers = Customer.objects.filter().order_by('account_no')
    context={
        'customers': customers,
    }
    return render(request, 'sheet/collection_sheet2.html', context)



