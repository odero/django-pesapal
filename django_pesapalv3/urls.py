# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = "django_pesapalv3"

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
