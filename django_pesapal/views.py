# Create your views here.

from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView


from .models import Transaction

import conf


class TransactionCompletedView(RedirectView):
    permanent = False
    url = reverse_lazy(conf.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        '''
        After Pesapal processes the transaction this will save the transaction and then redirect
        to whatever reidrect URL in your settings as `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.

        For further processing just create a `post_save` signal on the `Transaction` model.
        '''
        self.transaction_id = request.GET.get('pesapal_transaction_tracking_id', '')
        self.merchant_reference = request.GET.get('pesapal_merchant_reference', '')

        if self.transaction_id and self.merchant_reference:
            transaction = Transaction.objects.get_or_create(merchant_reference=self.merchant_reference, pesapal_transaction=self.transaction_id)

        return super(TransactionCompletedView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        url = reverse_lazy(conf.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL,
                           kwargs={'transaction_id': self.transaction_id, 'merchant_reference': self.merchant_reference})
        return url


