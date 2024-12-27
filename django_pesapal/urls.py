# -*- coding: utf-8 -*-

try:
    from django.urls import re_path as url
except ImportError:
    # support django<4.0
    from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^transaction/completed/$",
        views.TransactionCompletedView.as_view(),
        name="transaction_completed",
    ),
    url(
        r"^transaction/status/$",
        views.TransactionStatusView.as_view(),
        name="transaction_status",
    ),
    url(r"^transaction/ipn/$", views.IPNCallbackView.as_view(), name="transaction_ipn"),
]
