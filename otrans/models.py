from datetime import date, timezone
import random
import string
from django.db import models
from primary_setup.models import OutLoan, Director, CustomUser, VoucherCategory
from django.utils import timezone


class Expense(models.Model):
    voucher_category = models.ForeignKey(VoucherCategory, on_delete=models.CASCADE)
    CustomerName = models.CharField(max_length=100)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    ExpenseBy = models.CharField(max_length=50)
    IsCalculateWithLossProfit = models.BooleanField(null=True, blank=True)
    ExpenseDate = models.DateField(null=True, blank=True)
    Note = models.CharField(max_length=200, null=True, blank=True)

class Income(models.Model):
    voucher_category = models.ForeignKey(VoucherCategory, on_delete=models.CASCADE)
    CustomerName = models.CharField(max_length=100)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    IncomeBy = models.CharField(max_length=50)
    IsCalculateWithLossProfit = models.BooleanField(null=True, blank=True)
    IncomeDate = models.DateField(null=True, blank=True)
    Note = models.CharField(max_length=200, null=True, blank=True)


class Deposit(models.Model):

    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    processed_by = models.CharField(max_length=50, null=True, blank=True)

    Date = models.DateField()
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Note = models.CharField(max_length=200, null=True, blank=True)


class Withdraw(models.Model):

    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    processed_by = models.CharField(max_length=50, null=True, blank=True)

    Date = models.DateField()
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Note = models.CharField(max_length=200, null=True, blank=True)


class Passbook(models.Model):

    customer = models.ForeignKey('app1.Customer', on_delete=models.CASCADE)
    Account = models.CharField(max_length=200)
    Category = models.CharField(max_length=200, null=True, blank=True)
    processed_by = models.CharField(max_length=50, null=True, blank=True)
    Date = models.DateField()
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Note = models.CharField(max_length=200, null=True, blank=True)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):            
        if not self.Date:
            self.Date = timezone.now().date()
        super().save(*args, **kwargs)


class SSM_Deposit(models.Model):

    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    processed_by = models.CharField(max_length=50, null=True, blank=True)

    Date = models.DateField()
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Note = models.CharField(max_length=200, null=True, blank=True)


class SSM_Withdraw(models.Model):

    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    processed_by = models.CharField(max_length=50, null=True, blank=True)

    Date = models.DateField()
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Note = models.CharField(max_length=200, null=True, blank=True)


class GetOutLoan(models.Model):

    account = models.ForeignKey(OutLoan, on_delete=models.CASCADE)
    date = models.DateField()
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    note = models.TextField(blank=True, null=True)
    processed_by = models.CharField(max_length=50, null=True, blank=True)
    VoucherID = models.CharField(max_length=50, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.VoucherID:
            self.VoucherID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
        if self.date is None:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.account} - {self.deposit_amount}"


class Salary(models.Model):
 
    date = models.DateField()
    year = models.PositiveIntegerField()
    month = models.CharField(max_length=100)
    staff_name = models.CharField(max_length=100)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payable = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    processed_by = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        self.payable = self.basic_salary + self.others + self.bonus - self.deduction
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.staff_name} - {self.year}/{self.month}'



class ProfitDistribution(models.Model):

    date = models.DateField()
    financial_year = models.CharField(max_length=20, default='July-June')
    year = models.CharField(max_length=9)
    profit_type = models.CharField(max_length=50)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    total_account = models.PositiveIntegerField()
    profit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    process_by = models.CharField(max_length=100, default='Admin')

    def __str__(self):
        return f"{self.date} - {self.profit_type}"
    


