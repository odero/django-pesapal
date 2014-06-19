# Create your views here.

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from .models import Transaction


class TransactionCompletedView(RedirectView):
    permanent = False
    url = settings.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        '''
        After Pesapal processes the transaction this will save the transaction and then redirect
        to whatever reidrect URL in your settings as `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.

        For further processing just create a `post_save` signal on the `Transaction` model.
        '''
        transaction_id = request.GET.get('pesapal_transaction_tracking_id', '')
        merchant_reference = request.GET.get('pesapal_merchant_reference', '')

        if transaction_id and merchant_reference:
            Transaction.objects.get_or_create(transaction_id=transaction_id, merchant_reference=merchant_reference)

        return super(TransactionCompletedView, self).get(request, *args, **kwargs)
