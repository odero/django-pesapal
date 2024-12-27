from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView

from django_pesapal.views import PaymentRequestMixin
from django_pesapalv3.views import PaymentRequestMixin as PaymentRequestMixinV3


class PaymentView(TemplateView, PaymentRequestMixin):
    """
    Make payment view
    """

    template_name = "testapp/payment.html"

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)

        order_info = {
            "amount": 10,
            "description": "Payment for X",
            "reference": 2,
            "email": "pesapal@example.com",
        }

        ctx["pesapal_url"] = self.get_payment_url(**order_info)
        return ctx


class PaymentViewV3(TemplateView, PaymentRequestMixinV3):
    """
    Make payment view
    """

    template_name = "testapp/payment.html"

    def get_context_data(self, **kwargs):
        ctx = super(PaymentViewV3, self).get_context_data(**kwargs)

        ipn = self.get_default_ipn()

        order_info = {
            "id": "DJP-APP-1234",
            "currency": "KES",
            "amount": 10,
            "description": "Payment for X",
            "callback_url": self.build_url(
                reverse(settings.PESAPAL_OAUTH_CALLBACK_URL)
            ),
            "notification_id": ipn,
            "billing_address": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "pesapal@example.com",
                "phone_number": "254712345678",
            },
        }
        req = self.submit_order_request(**order_info)
        ctx["pesapal_url"] = req["redirect_url"]
        return ctx
