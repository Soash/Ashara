from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


class CustomUser(AbstractUser):
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    house_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mobile_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    internet_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mobile = models.CharField(max_length=20, blank=True, null=True)

class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.bank_name

class BankTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bank_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    
    
    date = models.DateTimeField()
    note = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    attachment = models.FileField(upload_to='attachments', blank=True, null=True)
    # processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    # entry_date = models.DateTimeField(default=timezone.now)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = self.asset_type or ('credit' if self.transaction_type == 'deposit' else 'debit')
        super().save(*args, **kwargs)

class VoucherCategory(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inctive', 'Inactive'),
    ]
    CATEGORY_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    # category_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    voucher_name = models.CharField(max_length=100)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.voucher_name
    
class VoucherTransaction(models.Model):
    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    
    voucher = models.ForeignKey(VoucherCategory, on_delete=models.CASCADE, related_name='voucher_transactions')

    date = models.DateTimeField()
    note = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # attachment = models.FileField(upload_to='attachments', blank=True, null=True)
    # processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    # entry_date = models.DateTimeField(default=timezone.now)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = 'credit'
        super().save(*args, **kwargs)



class DPSScheme(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    scheme_name = models.CharField(max_length=100)
    payment_sequence = models.CharField(max_length=100)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.scheme_name





class Holiday(models.Model):
    event_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.event_name



class Director(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    director_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=100)
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    photo = models.ImageField(upload_to='director_photos', null=True, blank=True)

    def __str__(self):
        return self.director_name
    


class OutLoan(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    account_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    profession = models.CharField(max_length=50)
    address = models.CharField(max_length=20, null=True, blank=True)
    balance = models.FloatField()
    profit = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return f"{self.account_name}"
    





class SMSSetting(models.Model):
    STATUS_CHOICES = [
        ('on', 'On'),
        ('off', 'Off'),
    ]
    LANG_CHOICES = [
        ('bangla', 'Bangla'),
        ('english', 'English'),
    ]
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    language = models.CharField(max_length=20, choices=LANG_CHOICES, default='bangla')
    title = models.CharField(max_length=100)
    # content_english = models.TextField()
    content_bengali = models.TextField()

    def __str__(self):
        return f"{self.title}"

