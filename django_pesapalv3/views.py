import logging
import requests

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, RedirectView, TemplateView

from django_pesapal.models import Transaction

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

            # logger.debug(f"Auth token response: {res.json()}")
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

    def get_transaction_status(self):
        res = requests.get(
            settings.PESAPAL_GET_TRANSACTION_STATUS_URL
            + self.request.GET["OrderTrackingId"],
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self._get_token()['token']}",
            },
        )
        logger.debug(f"Transaction status response: {res.json()}")
        return res.json()


class PaymentResponseMixin(object):

    def build_url_params(self):
        url_params = QueryDict("", mutable=True)
        url_params.update(
            {
                "OrderMerchantReference": self.transaction.merchant_reference,
                "OrderTrackingId": self.transaction.pesapal_transaction,
            }
        )
        url_params = "?" + url_params.urlencode()
        return url_params

    def get_payment_status_url(self):
        status_url = reverse("django_pesapalv3:transaction_status")
        status_url += self.build_url_params()
        return status_url

    def get_order_completion_url(self):
        completed_url = reverse(settings.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL)
        completed_url += self.build_url_params()
        return completed_url


class TransactionCompletedView(PaymentResponseMixin, TemplateView):
    """
    After Pesapal processes the transaction this will save the transaction and
    then redirect to whatever redirect URL in your settings as
    `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.

    For further processing just create a `post_save` signal on the
    `Transaction` model.
    """

    template_name = "django_pesapal/post_payment.html"

    def get(self, request, *args, **kwargs):

        tracking_id = request.GET.get("OrderTrackingId", 0)
        merchant_reference = request.GET.get("OrderMerchantReference", 0)

        if tracking_id and merchant_reference:
            self.transaction, _ = Transaction.objects.get_or_create(
                merchant_reference=merchant_reference,
                pesapal_transaction=tracking_id,
            )

            return super(TransactionCompletedView, self).get(request, *args, **kwargs)
        else:
            return HttpResponse("Invalid request: Missing data", status=400)

    def get_context_data(self, **kwargs):

        ctx = super(TransactionCompletedView, self).get_context_data(**kwargs)

        ctx["transaction_completed_url"] = self.get_order_completion_url()
        ctx["transaction_status_url"] = self.get_payment_status_url()
        ctx["payment_status"] = self.transaction.payment_status

        if self.transaction.payment_status == Transaction.PENDING:
            message = _(
                "Your payment is being processed. We will notify you once it has completed"
            )
            ctx["payment_pending"] = True
        else:
            if self.transaction.payment_status == Transaction.COMPLETED:
                message = mark_safe(
                    _(
                        "Your payment has been successfully processed. "
                        "The page should automatically redirect in "
                        '<span class="countdown">3</span> seconds.'
                    )
                )
            elif self.transaction.payment_status == Transaction.FAILED:
                message = _(
                    "The processing of your payment failed. "
                    "Please contact the system administrator."
                )
            else:
                # INVALID
                message = _("The transaction details provided were invalid.")

        ctx["message"] = message
        return ctx


class UpdatePaymentStatusMixin(PaymentRequestMixin):
    def get_params(self):
        self.merchant_reference = self.request.GET.get("OrderMerchantReference", 0)
        self.transaction_id = self.request.GET.get("OrderTrackingId", None)

        params = {
            "OrderMerchantReference": self.merchant_reference,
            "OrderTrackingId": self.transaction_id,
        }

        return params

    def process_payment_status(self):
        params = self.get_params()

        self.transaction = get_object_or_404(
            Transaction,
            merchant_reference=self.merchant_reference,
            pesapal_transaction=self.transaction_id,
        )

        # check status from pesapal server
        response = self.get_transaction_status()

        self.transaction.payment_method = dict.get(response, "payment_method", "")
        self.transaction.payment_account = dict.get(response, "payment_account", "")
        self.transaction.amount = dict.get(response, "amount", 0)

        if response["status_code"] == 1:  # completed
            self.transaction.payment_status = Transaction.COMPLETED
        elif response["status_code"] == 2:  # failed
            self.transaction.payment_status = Transaction.FAILED
            logger.error("Failed Transaction: {}".format(self.transaction))
        elif response["status_code"] == 0:  # invalid
            self.transaction.payment_status = Transaction.INVALID
            logger.error("Invalid Transaction: {}".format(self.transaction))
        elif response["status_code"] == 3:  # reversed
            self.transaction.payment_status = Transaction.REVERSED
            logger.error("Reversed Transaction: {}".format(self.transaction))

        self.transaction.save()


class TransactionStatusView(UpdatePaymentStatusMixin, RedirectView):

    permanent = False
    url = None

    def get_redirect_url(self, *args, **kwargs):

        params = self.get_params()
        self.process_payment_status()

        # redirect back to Transaction completed view
        url = reverse("django_pesapalv3:transaction_completed")

        query_dict = QueryDict("", mutable=True)
        query_dict.update(params)
        url += "?" + query_dict.urlencode()

        return url


class IPNCallbackView(UpdatePaymentStatusMixin, PaymentResponseMixin, View):
    def build_ipn_response(self):
        params = self.get_params()
        params["pesapal_notification_type"] = self.request.GET.get(
            "pesapal_notification_type"
        )

        query_dict = QueryDict("", mutable=True)
        query_dict.update(params)
        response = query_dict.urlencode()
        return HttpResponse(response)

    def get(self, *args, **kwargs):
        self.process_payment_status()
        response = self.build_ipn_response()
        return response
