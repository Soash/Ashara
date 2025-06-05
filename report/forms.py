from django import forms
from primary_setup.models import CustomUser, DPSScheme, VoucherCategory
from report.models import UserLog





class CustomerSearchForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))



class DPSReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    scheme_name = forms.ModelChoiceField(
        queryset=DPSScheme.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=[('all', 'All'), ('active', 'Active'), ('closed', 'Closed')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account No.'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super(DPSReportForm, self).__init__(*args, **kwargs)
        
        # if user:
        self.fields['scheme_name'].queryset = DPSScheme.objects.filter()


class ShareReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account No.'}),
        required=False
    )



class VoucherReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=True
    )
    voucher_category = forms.ModelChoiceField(
        queryset=VoucherCategory.objects.filter(),  # add filter if you need like .filter(status='active')
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label="All"
    )

    def __init__(self, *args, **kwargs):
        super(VoucherReportForm, self).__init__(*args, **kwargs)
        self.fields['voucher_category'].queryset = VoucherCategory.objects.all()






class UESReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    staff = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UESReportForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['staff'].queryset = CustomUser.objects.filter()
    

class UWESReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UWESReportForm, self).__init__(*args, **kwargs)
        
        
    

class GeneralLedgerForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account No.'}),
        required=False
    )




class ReceivePaymentReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReceivePaymentReportForm, self).__init__(*args, **kwargs)
        

class ProfitLossReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfitLossReportForm, self).__init__(*args, **kwargs)


from django import forms
import calendar
from datetime import datetime

MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]
YEAR_CHOICES = [(str(year), str(year)) for year in range(2020, datetime.now().year + 1)]

class ReportForm(forms.Form):
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label='Month',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        label='Year',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class YearlyTopSheetForm(forms.Form):
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        label='Year',
        widget=forms.Select(attrs={'class': 'form-control'})
    )







class AccountStatementForm(forms.Form):
    account_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account No.'}),
        required=True
    )
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date From'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date To'}),
        required=False
    )

