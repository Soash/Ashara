from django import forms
from .models import Customer, DPS, DPSTransactionHistory, GeneralTransactionHistory, ShareACTransactionHistory
from .models import SavingsTransactionHistory
from primary_setup.models import BankTransaction, VoucherTransaction

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['password']
        widgets = {
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_photo': forms.FileInput(attrs={'class': 'form-control'}),
            
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_father': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_mother': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'customer_permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'customer_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'share_count': forms.NumberInput(attrs={'class': 'form-control', 'type': 'text'}),
            
            'mediator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recommender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'recommender_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'recommender_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'customer_signature': forms.FileInput(attrs={'class': 'form-control'}),
            'recommender_signature': forms.FileInput(attrs={'class': 'form-control'}),

            'nominee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_father': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_mother': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'nominee_permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'nominee_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'nominee_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'nominee_signature': forms.FileInput(attrs={'class': 'form-control'}),
            'president_signature': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(customer.account_number)
        if commit:
            customer.save()
        return customer
        
class GeneralTransactionForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    PURPOSE_CHOICES = [
        ('সাধারন জমা', 'সাধারন জমা'),
        ('এককালীন', 'এককালীন'),
        ('মাসিক', 'মাসিক'),
        ('মাসিক', 'মাসিক'),
        ('বিনিয়োগ', 'বিনিয়োগ'),
    ]

    month_note = forms.ChoiceField(choices=MONTH_CHOICES, required=True, label="Month")
    purpose_note = forms.ChoiceField(choices=PURPOSE_CHOICES, required=True, label="Purpose")

    class Meta:
        model = GeneralTransactionHistory
        fields = ['date', 'amount', 'month_note', 'purpose_note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SavingsTransactionForm(forms.ModelForm):
    class Meta:
        model = SavingsTransactionHistory
        fields = ['date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        
class DPSForm(forms.ModelForm):
    class Meta:
        model = DPS
        fields = [
            'created_date', 
            'dps_opening_charge',
            'dps_scheme',
            'start_installment', 
            'amount_per_installments', 
            'leger_no',
            'number_of_installments', 
            'installment_sequence', 
            'profit_percent',
            'profit_taka', 
            'fine_per_missed_installment', 
            'total_amount',
        ]
        labels = {
            'dps_opening_charge': 'DPS Opening Charge',
            'dps_scheme': 'DPS Scheme',
        }
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'text'}),
            'dps_opening_charge': forms.NumberInput(attrs={'placeholder': 'Opening Charge'}),
            'dps_scheme': forms.Select(attrs={'placeholder': 'Select DPS Scheme'}),
            'start_installment': forms.NumberInput(attrs={'placeholder': 'Start Installment'}),
            'amount_per_installments': forms.NumberInput(attrs={'placeholder': 'Input Amount Per Installment'}),
            'leger_no': forms.NumberInput(attrs={'placeholder': 'Leger No.'}),
            'installment_sequence': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total_amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'number_of_installments': forms.NumberInput(attrs={'placeholder': 'Input Number of Installments'}),
            'profit_percent': forms.NumberInput(attrs={'placeholder': 'Input Profit Percentage'}),
            'profit_taka': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Profit in Taka'}),
            'fine_per_missed_installment': forms.NumberInput(attrs={'placeholder': 'Fine per Missed Installment'}),
        }

class DPSTransactionForm(forms.ModelForm):
    class Meta:
        model = DPSTransactionHistory
        fields = ['date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
               
class ShareTransactionForm(forms.ModelForm):
    class Meta:
        model = ShareACTransactionHistory
        fields = ['date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'min': '0'}),
        }
        
class BankTransactionForm(forms.ModelForm):
    class Meta:
        model = BankTransaction
        fields = ['bank', 'transaction_type', 'date', 'note', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.TextInput(attrs={'placeholder': 'Note'}),
            'amount': forms.NumberInput(attrs={'min': '0'}),
        }

class VoucherTransactionForm(forms.ModelForm):
    
    class Meta:
        model = VoucherTransaction
        fields = ['voucher', 'date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'min': '0'}),
        }




        
class CustomerAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Customer
        fields = '__all__'


