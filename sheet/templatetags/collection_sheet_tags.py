from django import template
from app1.models import DPS, GeneralAC, SavingsAC, ShareAC
from django.db import models

register = template.Library()

@register.simple_tag
def customer_balance(customer):
    try:
        account = GeneralAC.objects.get(customer=customer)
        return account.balance
    except GeneralAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def customer_withdraw(customer):
    try:
        account = GeneralAC.objects.get(customer=customer)
        return account.total_withdraw
    except GeneralAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def customer_deposit(customer):
    try:
        account = GeneralAC.objects.get(customer=customer)
        return account.total_deposit
    except GeneralAC.DoesNotExist:
        return "N/A"


  
@register.simple_tag
def savings_balance(customer):
    try:
        account = SavingsAC.objects.get(customer=customer)
        return account.balance
    except SavingsAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def savings_withdraw(customer):
    try:
        account = SavingsAC.objects.get(customer=customer)
        return account.total_withdraw
    except SavingsAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def savings_deposit(customer):
    try:
        account = SavingsAC.objects.get(customer=customer)
        return account.total_deposit
    except SavingsAC.DoesNotExist:
        return "N/A"



@register.simple_tag
def dps_balance(customer):
    try:
        account = DPS.objects.get(customer=customer)
        return account.balance
    except DPS.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def dps_deposit(customer):
    try:
        account = DPS.objects.get(customer=customer)
        return account.total_deposit
    except DPS.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def dps_withdraw(customer):
    try:
        account = DPS.objects.get(customer=customer)
        return account.total_withdraw
    except DPS.DoesNotExist:
        return "N/A"
    


@register.simple_tag
def share_balance(customer):
    try:
        account = ShareAC.objects.get(customer=customer)
        return account.balance
    except ShareAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def share_deposit(customer):
    try:
        account = ShareAC.objects.get(customer=customer)
        return account.deposit
    except ShareAC.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def share_withdraw(customer):
    try:
        account = ShareAC.objects.get(customer=customer)
        return account.withdraw
    except ShareAC.DoesNotExist:
        return "N/A"


@register.simple_tag
def total_customer_balance(customers):
    total = GeneralAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('balance'))['total']
    return total if total else 0

@register.simple_tag
def total_customer_withdraw(customers):
    total = GeneralAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_withdraw'))['total']
    return total if total else 0

@register.simple_tag
def total_customer_deposit(customers):
    total = GeneralAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_deposit'))['total']
    return total if total else 0



@register.simple_tag
def total_savings_balance(customers):
    total = SavingsAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('balance'))['total']
    return total if total else 0
@register.simple_tag
def total_savings_withdraw(customers):
    total = SavingsAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_withdraw'))['total']
    return total if total else 0
@register.simple_tag
def total_savings_deposit(customers):
    total = SavingsAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_deposit'))['total']
    return total if total else 0



@register.simple_tag
def total_dps_balance(customers):
    total = DPS.objects.filter(customer__in=customers).aggregate(total=models.Sum('balance'))['total']
    return total if total else 0
@register.simple_tag
def total_dps_withdraw(customers):
    total = DPS.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_withdraw'))['total']
    return total if total else 0
@register.simple_tag
def total_dps_deposit(customers):
    total = DPS.objects.filter(customer__in=customers).aggregate(total=models.Sum('total_deposit'))['total']
    return total if total else 0



@register.simple_tag
def total_share_balance(customers):
    total = ShareAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('balance'))['total']
    return total if total else 0
@register.simple_tag
def total_share_withdraw(customers):
    total = ShareAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('withdraw'))['total']
    return total if total else 0
@register.simple_tag
def total_share_deposit(customers):
    total = ShareAC.objects.filter(customer__in=customers).aggregate(total=models.Sum('deposit'))['total']
    return total if total else 0






