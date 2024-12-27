"""
Settings file for django-pesapalv3
"""

from django.conf import settings

PESAPAL_DEMO_ENDPOINT = "https://cybqa.pesapal.com/pesapalv3/api"
PESAPAL_PROD_ENDPOINT = " https://pay.pesapal.com/v3/api"


if settings.configured:
    PESAPAL_DEMO = getattr(settings, "PESAPAL_DEMO", True)
    PESAPAL_ENDPOINT = PESAPAL_DEMO_ENDPOINT if PESAPAL_DEMO else PESAPAL_PROD_ENDPOINT

    PESAPAL_IPN_NOTIFICATION_TYPE = getattr(
        settings, "PESAPAL_IPN_NOTIFICATION_TYPE", "POST"
    )

    PESAPAL_GET_IPNS_URL = getattr(
        settings, "PESAPAL_GET_IPNS_URL", f"{PESAPAL_ENDPOINT}/URLSetup/GetIpnList"
    )
    PESAPAL_AUTH_URL = getattr(
        settings, "PESAPAL_AUTH_URL", f"{PESAPAL_ENDPOINT}/Auth/RequestToken"
    )
    PESAPAL_IPN_REGISTRATION_URL = getattr(
        settings,
        "PESAPAL_IPN_REGISTRATION_URL",
        f"{PESAPAL_ENDPOINT}/URLSetup/RegisterIPN",
    )
    PESAPAL_ORDER_SUBMISSION_URL = getattr(
        settings,
        "PESAPAL_ORDER_SUBMISSION_URL",
        f"{PESAPAL_ENDPOINT}/Transactions/SubmitOrderRequest",
    )
    PESAPAL_GET_TRANSACTION_STATUS_URL = getattr(
        settings,
        "PESAPAL_GET_TRANSACTION_STATUS_URL",
        f"{PESAPAL_ENDPOINT}/Transactions/GetTransactionStatus?orderTrackingId=",
    )
    PESAPAL_GET_IPNS_URL = getattr(
        settings, "PESAPAL_GET_IPNS_URL", f"{PESAPAL_ENDPOINT}/URLSetup/GetIpnList"
    )
    PESAPAL_IPN_URL = getattr(settings, "PESAPAL_IPN_URL", "django_pesapalv3:transaction_ipn")

    PESAPAL_CONSUMER_KEY = getattr(settings, "PESAPAL_CONSUMER_KEY")
    PESAPAL_CONSUMER_SECRET = getattr(settings, "PESAPAL_CONSUMER_SECRET")

    PESAPAL_CALLBACK_URL = getattr(
        settings, "PESAPAL_CALLBACK_URL", "django_pesapalv3:transaction_completed"
    )

    PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = getattr(
        settings, "PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL", "/v3/"
    )

    PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = getattr(
        settings,
        "PESAPAL_TRANSACTION_FAILED_REDIRECT_URL",
        PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL,
    )

    PESAPAL_REDIRECT_WITH_REFERENCE = False

    PESAPAL_TRANSACTION_MODEL = getattr(
        settings, "PESAPAL_TRANSACTION_MODEL", "django_pesapal.Transaction"
    )
