from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import CustomTransactionCompletedView

urlpatterns = patterns(
    '',
    url(r'^transaction/completed/$', login_required(CustomTransactionCompletedView.as_view()), name='transaction_completed'),
)
