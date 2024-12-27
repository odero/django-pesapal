import logging
import requests

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.views.generic import TemplateView

from . import conf as settings

logger = logging.getLogger(__name__)


# Create your views here.
class PaymentRequestMixin(object):
    def _get_token(self):
        """
        Authenticates and returns token
        """
        # TODO: consider encrypting
        auth_token = cache.get("pesapal_auth_token")
        if not auth_token:
            logger.debug(f"Calling auth token endpoint: {settings.PESAPAL_AUTH_URL}")
            res = requests.post(
                settings.PESAPAL_AUTH_URL,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json={
                    "consumer_key": settings.PESAPAL_CONSUMER_KEY,
                    "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
                },
            )

            logger.debug(f"Auth token response: {res.json()}")
            auth_token = res.json()
            cache.set("pesapal_auth_token", auth_token, 60 * 4)

        return auth_token

    def get_default_ipn(self):
        """
        Returns default IPN
        """
        ipn = cache.get("pesapal_ipn")
        if not ipn:
            logger.debug(f"Calling IPN endpoint: {settings.PESAPAL_GET_IPNS_URL}")
            res = requests.get(
                settings.PESAPAL_GET_IPNS_URL,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self._get_token()['token']}",
                },
            )
            ipns = res.json()
            logger.debug(f"IPN response: {ipns}")
            if len(ipns) == 0:
                ipn = self._register_ipn()
            else:
                ipn = ipns[0]["ipn_id"]

            cache.set("pesapal_ipn", ipn, 60 * 60 * 24)

        return ipn

    def _register_ipn(self):
        """
        Registers IPN
        Sample response:
        {
            "url": "https://myapplication.com/ipn",
            "created_date": "2024-06-14T07:50:22.2825997Z",
            "ipn_id": "84740ab4-3cd9-47da-8a4f-dd1db53494b5",
            "notification_type": 0,
            "ipn_notification_type_description": "GET",
            "ipn_status": 1,
            "ipn_status_description": "Active",
            "error": null,
            "status": "200"
        }
        """
        url = self.build_url(reverse(settings.PESAPAL_IPN_URL))
        data = {
            "ipn_notification_type": settings.PESAPAL_IPN_NOTIFICATION_TYPE or "POST",
            "url": url,
        }
        logger.debug(f"Registering IPN: {settings.PESAPAL_IPN_REGISTRATION_URL}")
        logger.debug(f"IPN data: {data}")

        res = requests.post(
            settings.PESAPAL_IPN_REGISTRATION_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self._get_token()['token']}",
            },
            json=data,
        )
        res_json = res.json()
        logger.debug(f"IPN registration response: {res_json}")

        cache.set("pesapal_ipn", res_json["ipn_id"], 60 * 60 * 24)

        return res_json["ipn_id"]

    def build_url(self, path=None):
        if self.request:
            url = self.request.build_absolute_uri(path)
        else:
            current_site = Site.objects.get_current()
            protocol = "http" if settings.PESAPAL_DEMO else "https"
            url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                path,
            )
        return url

    def submit_order_request(self, **kwargs):
        """
        Submits order request
        Sample response:
        {
            "order_tracking_id": "b945e4af-80a5-4ec1-8706-e03f8332fb04",
            "merchant_reference": "TEST1515111119",
            "redirect_url": "https://cybqa.pesapal.com/pesapaliframe/PesapalIframe3/Index/?OrderTrackingId=b945e4af-80a5-4ec1-8706-e03f8332fb04",
            "error": null,
            "status": "200"
        }
        """
        params = {}
        params.update(**kwargs)
        logger.debug(f"Order request endpoint: {settings.PESAPAL_ORDER_SUBMISSION_URL}")
        logger.debug(f"Order request params: {params}")
        res = requests.post(
            settings.PESAPAL_ORDER_SUBMISSION_URL,
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {self._get_token()['token']}",
            },
            json=params,
        )
        logger.debug(f"Order request response: {res.json()}")
        return res.json()


class PaymentResponseMixin(object):
    def handle_ipn(self):
        """
        Sample payload:
        {
            "OrderNotificationType":"IPNCHANGE",
            "OrderTrackingId":"b945e4af-80a5-4ec1-8706-e03f8332fb04",
            "OrderMerchantReference":"TEST1515111119"
        }
        """
        pass

    def get_transaction_status(self):
        res = requests.get(
            settings.PESAPAL_GET_TRANSACTION_STATUS_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self._get_token()['token']}",
            },
        )

        return res.json()


class TransactionCompletedView(PaymentResponseMixin, TemplateView):
    template_name = "transaction_completed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transaction"] = self.get_transaction_status()
        return context
