from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', views.TransactionCompletedView.as_view(), name='transaction_completed'),
    url(r'^transaction/status/$', views.TransactionStatusView.as_view(), name='transaction_status'),
    url(r'^transaction/ipn/$', views.IPNCallbackView.as_view(), name='transaction_ipn'),
)
