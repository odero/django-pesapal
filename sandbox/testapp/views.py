import uuid
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView

from django_pesapal.views import PaymentRequestMixin
from django_pesapalv3.views import PaymentRequestMixin as PaymentRequestMixinV3


class PaymentView(TemplateView, PaymentRequestMixin):
    """
    Make payment view
    """

    # template_name = "django_pesapal/payment.html"
    template_name = "testapp/payment.html"

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)
        ctx["pesapal_url"] = self.get_pesapal_payment_iframe()
        return ctx

    def get_pesapal_payment_iframe(self):
        order_info = {
            "amount": 10,
            "description": "Payment for X",
            "reference": 2,
            "email": "pesapal@example.com",
        }

        return self.get_payment_url(**order_info)


class PaymentViewV3(TemplateView, PaymentRequestMixinV3):
    """
    Make payment view
    """

    # template_name = "django_pesapal/payment.html"
    template_name = "testapp/payment.html"

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)
        ctx["pesapal_url"] = self.get_pesapal_payment_iframe()
        return ctx

    def get_pesapal_payment_iframe(self):
        """
        Authenticates with pesapal to get the payment iframe src
        """
        # you can replace this with your own ipn registration method
        ipn = self.get_default_ipn()

        order_info = {
            # replace id with a valid merchant id
            "id": self.request.GET.get("id", uuid.uuid4().hex),
            "currency": "KES",
            "amount": 10,
            "description": "Payment for X",
            "callback_url": self.build_url(
                reverse("django_pesapalv3:transaction_completed")
            ),
            "notification_id": ipn,
            "billing_address": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "pesapal@example.com",
            },
        }
        req = self.submit_order_request(**order_info)
        return req["redirect_url"]
