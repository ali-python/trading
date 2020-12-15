from django.conf import settings

def settings_context(request):
    context = {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_SHORT_NAME': settings.COMPANY_SHORT_NAME,
        'COMPANY_SLOGAN': settings.COMPANY_SLOGAN,
        'FULL_ADDRESS': settings.FULL_ADDRESS,
        'SHORT_ADDRESS': settings.SHORT_ADDRESS,
        'PRIMARY_CONTACT': settings.PRIMARY_CONTACT,
        'SECONDARY_CONTACT': settings.SECONDARY_CONTACT,
        'LINE_CONTACT': settings.LINE_CONTACT
    }
    return context
