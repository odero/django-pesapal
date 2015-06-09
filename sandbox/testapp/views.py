from django.views.generic import TemplateView
from django_pesapal.views import PaymentRequestMixin
from django_pesapal.models import Transaction


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


class ResponseView(TemplateView, PaymentRequestMixin):
    """
    Payment Response View
    """
    template_name = 'testapp/response.html'

    def get_context_data(self, **kwargs):
        ctx = super(ResponseView, self).get_context_data(**kwargs)

        merchant_reference = self.request.GET.get('merchant_reference', '')

        if merchant_reference:
            try:
                txn = Transaction.objects.get(merchant_reference=merchant_reference)
                params = {
                    'pesapal_merchant_reference': txn.merchant_reference,
                    'pesapal_transaction_tracking_id': txn.pesapal_transaction,
                }

                # In production, the following call should be made asynchronously with something like celery
                ctx['response'] = self.get_payment_status(**params)
            except Transaction.DoesNotExist, e:
                # In production, deal with this dont just print e
                print e

        return ctx