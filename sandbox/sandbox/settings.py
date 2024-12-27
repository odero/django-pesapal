"""
Django settings for sandbox project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

# sys.path.append()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.dirname(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "53(upox#u=f-0#5ue!)owq&-h#u)7z(z-nel&#(*tqhr@e3-u9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "testapp",
    "django_pesapal",
    "django_pesapalv3",
)


MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "sandbox.urls"

WSGI_APPLICATION = "sandbox.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"

# Pesapal API configuration
# Obtain test keys by creating a merchant account here http://demo.pesapal.com/


TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {
        "django_pesapal": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "django_pesapalv3": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}

PESAPAL_DEMO = True
PESAPAL_OAUTH_CALLBACK_URL = "transaction_completed"
PESAPAL_OAUTH_SIGNATURE_METHOD = "SignatureMethod_HMAC_SHA1"
PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = "paymentv3"
PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL
PESAPAL_ITEM_DESCRIPTION = False
PESAPAL_TRANSACTION_MODEL = "django_pesapal.Transaction"
PESAPAL_CONSUMER_KEY = "INSERT_YOUR_KEY"
PESAPAL_CONSUMER_SECRET = "7JDPmAvcnIGN7E4KJeB1c8M8e2s="

PESAPAL_IPN_NOTIFICATION_TYPE = "GET"
PESAPAL_IPN_URL = "django_pesapalv3:transaction_ipn"
# Override pesapal keys

try:
    from local_config import *
except ImportError:
    pass


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
