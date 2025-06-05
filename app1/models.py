from django.db import models
import random
import string
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from otrans.models import Passbook
from primary_setup.models import Holiday, CustomUser, DPSScheme, Bank
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, account_number, password=None, **extra_fields):

        user = self.model(account_number=account_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    
class Customer(AbstractBaseUser):
 
    joining_date = models.DateField()
    account_number = models.CharField(max_length=50)
    customer_photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_father = models.CharField(max_length=100, blank=True, null=True)
    customer_mother = models.CharField(max_length=100, blank=True, null=True)
    
    customer_current_address = models.TextField(blank=True, null=True)
    customer_permanent_address = models.TextField(blank=True, null=True)
    customer_nid = models.CharField(max_length=20, blank=True, null=True)
    customer_mobile = models.CharField(max_length=11, blank=True, null=True)
    
    share_count = models.PositiveIntegerField(blank=True, null=True)
    mediator_name = models.CharField(max_length=100, blank=True, null=True)
    recommender_name = models.CharField(max_length=100, blank=True, null=True)
    recommender_relation = models.CharField(max_length=100, blank=True, null=True)
    recommender_mobile = models.CharField(max_length=11, blank=True, null=True)

    customer_signature = models.ImageField(upload_to="signatures/", blank=True, null=True)
    recommender_signature = models.ImageField(upload_to="signatures/", blank=True, null=True)



    nominee_name = models.CharField(max_length=100, blank=True, null=True)
    nominee_father = models.CharField(max_length=100, blank=True, null=True)
    nominee_mother = models.CharField(max_length=100, blank=True, null=True)
    nominee_relation = models.CharField(max_length=100, blank=True, null=True)
    
    nominee_current_address = models.TextField(blank=True, null=True)
    nominee_permanent_address = models.TextField(blank=True, null=True)
    
    nominee_nid = models.CharField(max_length=20, blank=True, null=True)
    nominee_mobile = models.CharField(max_length=15, blank=True, null=True)
    
    nominee_photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    nominee_signature = models.ImageField(upload_to="signatures/", blank=True, null=True)
    president_signature = models.ImageField(upload_to="signatures/", blank=True, null=True)

    USERNAME_FIELD = 'account_number'
    

   
@receiver(post_save, sender=Customer)
def create_general_ac(sender, instance, created, **kwargs):
    if created:
        GeneralAC.objects.create(customer=instance, balance=0)
        SavingsAC.objects.create(customer=instance, balance=0)
        

class GeneralAC(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Close', 'Close'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_deposit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_withdraw = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.customer.customer_name} - {self.status}"

class GeneralTransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)

    account = models.ForeignKey(GeneralAC, on_delete=models.CASCADE, related_name='general_transaction_history')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200, null=True, blank=True)
    month_note = models.CharField(max_length=200, null=True, blank=True)
    purpose_note = models.CharField(max_length=200, null=True, blank=True)
    VoucherID = models.CharField(max_length=50, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = self.asset_type or ('debit' if self.transaction_type == 'deposit' else 'credit')
        super().save(*args, **kwargs)


class SavingsAC(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Close', 'Close'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_deposit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_withdraw = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.customer.customer_name} - {self.status}"

class SavingsTransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]

    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    
    account = models.ForeignKey(SavingsAC, on_delete=models.CASCADE, related_name='savings_transaction_history')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200, null=True, blank=True)
    VoucherID = models.CharField(max_length=50, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = self.asset_type or ('debit' if self.transaction_type == 'deposit' else 'credit')
        super().save(*args, **kwargs)




class DPS(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    created_date = models.DateField()
    dps_scheme = models.ForeignKey(DPSScheme, on_delete=models.CASCADE, default=1)

    amount_per_installments = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_installments = models.IntegerField()

    profit_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    profit_taka = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_per_missed_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    dps_opening_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    dps_closing_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    start_installment = models.IntegerField(default=0)
    leger_no = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    installment_sequence = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=15, unique=True, editable=False)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    total_deposit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_withdraw = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='active')

    @property
    def paid_installments(self):
        return self.dps_installment_schedules.filter(installment_status='paid').count()
    
    @property
    def due(self):
        return self.total_amount - self.balance

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        if not self.start_date:
            self.start_date = self.created_date + timedelta(days=self.start_installment)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"DPS : {self.transaction_id}"


    def generate_installment_schedule(self):
        schedule = []
        
        start_date = self.created_date + timedelta(days=self.start_installment)
        current_date = start_date
        holidays = Holiday.objects.values_list('date', flat=True)

        # Determine the interval based on the DPS scheme's payment sequence
        if self.dps_scheme.payment_sequence:
            interval_days = self.dps_scheme.payment_sequence
        else:
            interval_days = 1  # Default to daily if no payment_sequence is provided

        for i in range(self.number_of_installments):
            skipped_date = None

            # Determine the next installment date based on the payment sequence
            current_date += timedelta(days=int(interval_days))

            # Skip weekends and holidays
            while current_date.weekday() in [4] or current_date in holidays:  # 5 is Saturday, 6 is Sunday
                skipped_date = current_date
                current_date += timedelta(days=1)

            # Create an installment schedule
            schedule.append(DPSInstallmentSchedule(
                dps=self,
                installment_number=i + 1,
                due_date=current_date,
                amount=self.amount_per_installments,
                skipped_due_date=skipped_date
            ))

        # Bulk create the schedule and update end_date
        DPSInstallmentSchedule.objects.bulk_create(schedule)
        self.end_date = schedule[-1].due_date if schedule else self.start_date
        self.save()
        return schedule

class DPSInstallmentSchedule(models.Model):
    STATUS_CHOICES = [
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('---', '---'),
    ]
    dps = models.ForeignKey(DPS, on_delete=models.CASCADE, related_name='dps_installment_schedules')
    installment_number = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    skipped_due_date = models.DateField(blank=True, null=True)
    installment_status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='due')


    def __str__(self):
        return f"Installment {self.installment_number} for DPS {self.dps.transaction_id} - Due {self.due_date}"

    @property
    def is_skipped(self):
        return self.skipped_due_date is not None
    
class DPSTransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    
    account = models.ForeignKey(DPS, on_delete=models.CASCADE, related_name='dps_transaction_history')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    
    date = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    VoucherID = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = self.asset_type or ('debit' if self.transaction_type == 'deposit' else 'credit')
        super().save(*args, **kwargs)



 
class ShareAC(models.Model):
    share_id = models.PositiveIntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    nominee = models.CharField(max_length=255)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    get_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.share_id:
            last_share = ShareAC.objects.order_by('-share_id').first()
            self.share_id = (last_share.share_id + 1) if last_share else 1001
        super().save(*args, **kwargs)

class ShareACTransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]
    ASSET_TYPE_CHOICES = [
        ('debit', 'debit'),
        ('credit', 'credit'),
    ]
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    account = models.ForeignKey(ShareAC, on_delete=models.CASCADE, related_name='share_ac_transaction_history')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=200, null=True, blank=True)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        self.asset_type = self.asset_type or ('debit' if self.transaction_type == 'deposit' else 'credit')
        super().save(*args, **kwargs)

    


class Package(models.Model):
    client_id = models.CharField(max_length=255, default="1234", blank=True, null=True)
    status = models.CharField(max_length=50, default="Active", blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    expired_date = models.DateField(blank=True, null=True)
    billing_cycle = models.CharField(max_length=50, default="Monthly", blank=True, null=True)
    package_name = models.CharField(max_length=100, blank=True, null=True)
    limit_customer = models.CharField(max_length=100, default="100", blank=True, null=True)

    def __str__(self):
        return f"{self.package_name} ({self.limit_customer} Members)"


class Logo(models.Model):
    image = models.ImageField(upload_to='logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    somity_name = models.CharField(max_length=255)  # Added field for somity name

    def __str__(self):
        return f"Logo {self.id} - {self.somity_name}"

    