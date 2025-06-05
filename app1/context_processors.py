from primary_setup.models import CustomUser
from .models import Customer, Logo
from django.contrib.auth.models import AnonymousUser
from django.utils import translation
from sms.models import DomainReport
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import base64

def branches(request):
    language = request.session.get('language', 'en')
    translation.activate(language)
    request.LANGUAGE_CODE = language
    return {
        'branches': "Ashara"
    }



def active_branch_processor(request):
    
    logo = Logo.objects.first()
    try:
        somity_name = Logo.objects.first().somity_name
    except (Logo.DoesNotExist, AttributeError):
        somity_name = "Unknown Somity"
            
    return {'active_branch': "Ashara", 'logo': logo, 'somity_name': somity_name}

