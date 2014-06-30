from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import TransactionCompletedView

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', login_required(TransactionCompletedView.as_view()), name='transaction_completed'),
)
