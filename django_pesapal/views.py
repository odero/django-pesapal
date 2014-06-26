# Create your views here.

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from django.db.models.loading import get_model

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
        transaction_id = request.GET.get('pesapal_transaction_tracking_id', '')
        merchant_reference = request.GET.get('pesapal_merchant_reference', '')

        if transaction_id and merchant_reference:
            transaction, created = Transaction.objects.get_or_create(pk=merchant_reference, pesapal_transaction_id=transaction_id)

        return super(TransactionCompletedView, self).get(request, *args, **kwargs)
