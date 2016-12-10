# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^transaction/completed/$',
        views.TransactionCompletedView.as_view(),
        name='transaction_completed'
    ),
    url(
        r'^transaction/status/$',
        views.TransactionStatusView.as_view(),
        name='transaction_status'
    ),
    url(
        r'^transaction/ipn/$',
        views.IPNCallbackView.as_view(),
        name='transaction_ipn'
    ),
]
