'''
Settings file for django-pesapal
'''
from django.conf import settings

if settings.configured:
    PESAPAL_DEMO = getattr(settings, 'PESAPAL_DEMO', True)

    if PESAPAL_DEMO:
        PESAPAL_IFRAME_LINK = getattr(settings, 'PESAPAL_IFRAME_LINK', 'http://demo.pesapal.com/api/PostPesapalDirectOrderV4')
    else:
        PESAPAL_IFRAME_LINK = getattr(settings, 'PESAPAL_IFRAME_LINK', 'https://www.pesapal.com/api/PostPesapalDirectOrderV4')

    PESAPAL_CONSUMER_KEY = getattr(settings, 'PESAPAL_CONSUMER_KEY', '')
    PESAPAL_CONSUMER_SECRET = getattr(settings, 'PESAPAL_CONSUMER_SECRET', '')

    PESAPAL_OAUTH_CALLBACK_URL = getattr(settings, 'PESAPAL_OAUTH_CALLBACK_URL', 'transaction_completed')

    PESAPAL_OAUTH_SIGNATURE_METHOD = getattr(settings, 'PESAPAL_OAUTH_SIGNATURE_METHOD', 'SignatureMethod_HMAC_SHA1')

    PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = getattr(settings, 'PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL', '')

    PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = getattr(settings, 'PESAPAL_TRANSACTION_FAILED_REDIRECT_URL', PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL)
