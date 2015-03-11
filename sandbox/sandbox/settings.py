"""
Django settings for sandbox project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
sys.path.append('..')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '53(upox#u=f-0#5ue!)owq&-h#u)7z(z-nel&#(*tqhr@e3-u9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testapp',
    'django_pesapal'
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sandbox.urls'

WSGI_APPLICATION = 'sandbox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Pesapal API configuration
# Obtain test keys by creating a merchant account here http://demo.pesapal.com/

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_pesapal': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

PESAPAL_CONSUMER_KEY = 'consumer_key'
PESAPAL_CONSUMER_SECRET = 'consumer_key_secret'
PESAPAL_DEMO=True
if PESAPAL_DEMO:
    PESAPAL_IFRAME_LINK = 'http://demo.pesapal.com/api/PostPesapalDirectOrderV4'
    PESAPAL_QUERY_STATUS_LINK = 'http://demo.pesapal.com/API/QueryPaymentStatus'
else:
    PESAPAL_IFRAME_LINK = 'https://www.pesapal.com/api/PostPesapalDirectOrderV4'
    PESAPAL_QUERY_STATUS_LINK = 'https://www.pesapal.com/API/QueryPaymentStatus'
PESAPAL_OAUTH_CALLBACK_URL ='transaction_completed'
PESAPAL_OAUTH_SIGNATURE_METHOD ='SignatureMethod_HMAC_SHA1'
PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = 'transaction_status'
PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = ''
PESAPAL_ITEM_DESCRIPTION = False
PESAPAL_TRANSACTION_MODEL = 'testapp.Transaction'

# Override pesapal keys

try:
    from local_config import *
except ImportError:
    pass