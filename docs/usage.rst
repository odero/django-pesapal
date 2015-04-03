========
Usage
========

Take a look at the sandbox app for a quick overview on how to use `django-pesapal`.

To use django-pesapal in a project::

    from django.views.generic import TemplateView
    from django_pesapal.views import PaymentRequestMixin
    from django_pesapal.models import Transaction

    class PaymentView(TemplateView, PaymentRequestMixin):
        """
        This view returns secure payment form from pesapal
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

            # get_payment_url returns the URL of the secure payment form from pesapal
            # You can use this URL in an iframe
            ctx['pesapal_url'] = self.get_payment_url(**order_info)
            return ctx


    class ResponseView(TemplateView, PaymentRequestMixin):
        """
        Use this view if you want to find out the status of a transaction
        """
        template_name = 'testapp/response.html'

        def get(self, request, *args, **kwargs):
                self.merchant_reference = request.GET.get('merchant_reference', '')

                return super(ResponseView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            ctx = super(ResponseView, self).get_context_data(**kwargs)

            if self.merchant_reference:
                try:
                    txn = Transaction.objects.get(merchant_reference=self.merchant_reference)
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
