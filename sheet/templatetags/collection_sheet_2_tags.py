from django import template
from app1.models import DPS, GeneralAC, SavingsAC
from django.db import models
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def savings_balance(customer):
    try:
        account = GeneralAC.objects.get(customer=customer)
        return account.balance
    except GeneralAC.DoesNotExist:
        return 0

@register.simple_tag
def savings_target(customer):
    try:
        account = GeneralAC.objects.get(customer=customer)
        return account.regular_target
    except GeneralAC.DoesNotExist:
        return 0

@register.simple_tag
def special_balance(customer):
    try:
        account = SavingsAC.objects.get(customer=customer)
        return account.balance
    except SavingsAC.DoesNotExist:
        return 0

@register.simple_tag
def special_target(customer):
    try:
        account = SavingsAC.objects.get(customer=customer)
        return account.regular_target
    except SavingsAC.DoesNotExist:
        return 0


@register.simple_tag
def total_data_count(customer):
    dps_count = DPS.objects.filter(customer=customer).count()
    x = dps_count + 2
    return x

@register.simple_tag


@register.simple_tag
def add_dps(customer):
    dps = DPS.objects.filter(customer=customer)
    
    details_html = ""
    for info in dps:
        details_html += f'''<tr>
        <td>DPS</td>
        <td class="total">{info.total_amount}</td>
        <td class="balance">{info.balance}</td> 
        <td class="due">{info.due}</td>
        <td class="inst">{info.amount_per_installments}</td>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
        </tr>'''
    return mark_safe(details_html)


