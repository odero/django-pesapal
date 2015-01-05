from django.views.generic import TemplateView
from django_pesapal.app import get_payment_url


class PaymentView(TemplateView):
    """
        Make payment view
    """
    template_name = 'testapp/payment.html'

    def get_context_data(self, **kwargs):
        ctx = super(PaymentView, self).get_context_data(**kwargs)

        order_info = {
            'amount': 100,
            'description': 'Payment for X',
            'reference': 2,
            'email': 'pesapal@example.com'
        }

        ctx['pesapal_url'] = get_payment_url(request=self.request, **order_info)
        return ctx



class ResponseView(TemplateView):
    """
        Payment Response View
    """
    template_name = 'testapp/response.html'

    def get(self, request, *args, **kwargs):
            self.transaction_id = kwargs['transaction_id']
            self.token = kwargs['merchant_reference']

            return super(ResponseView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ResponseView, self).get_context_data(**kwargs)
        ctx['payment_status'] = 'Payment Pending'
        return ctx