
from django.conf import settings
from django.views.generic import TemplateView

from django_pesapal.views import PaymentRequestMixin


class PaymentView(TemplateView, PaymentRequestMixin):
    """
    Make payment view
    """
    template_name = 'testapp/payment.html'

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)

        order_info = {
            'amount': 10,
            'description': 'Payment for X',
            'reference': 2,
            'email': 'pesapal@example.com'
        }

        ctx['pesapal_url'] = self.get_payment_url(**order_info)
        return ctx
