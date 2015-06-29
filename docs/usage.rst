======
Usage
======

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
                'first_name': 'Some',
                'last_name': 'User',
                'amount': 100,
                'description': 'Payment for X',
                'reference': 2,
                'email': 'pesapal@example.com'
            }

            # get_payment_url returns the URL of the secure payment form from pesapal
            # You can use this URL in an iframe
            ctx['pesapal_url'] = self.get_payment_url(**order_info)
            return ctx


Once processing is complete the user will be redirected to the intermediate processing where
they can update check the status of the payment

**NOTE:** You can override the intermediate (`post_payment.html`) processing template if you 
need to have a customized look.
