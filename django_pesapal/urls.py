from django.conf.urls import patterns, url

from .views import TransactionCompletedView

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', TransactionCompletedView.as_view(), name='transaction_completed'),
)
