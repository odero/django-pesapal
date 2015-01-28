from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import TransactionCompletedView, IpnResponseHandlerView

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', TransactionCompletedView.as_view(), name='transaction_completed'),
    url(r'^transaction/notification/$', csrf_exempt(IpnResponseHandlerView.as_view()), name='transaction_notification')
)
