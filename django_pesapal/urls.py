from django.conf.urls import patterns, url

from .views import TransactionCompletedView, IpnResponseHandlerView

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', TransactionCompletedView.as_view(), name='transaction_completed'),
    url(r'^transaction/notification/$', IpnResponseHandlerView.as_view(), name='transaction_notification')
)
