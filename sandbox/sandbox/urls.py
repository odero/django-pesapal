from django.conf.urls import patterns, include, url

from django.contrib import admin
from testapp.views import PaymentView, ResponseView
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PaymentView.as_view(), name='payment'),
    url(r'^', include('django_pesapal.urls')),
    url(r'^response/(?P<merchant_reference>\d+)/$', ResponseView.as_view(), name='transaction_status'),

)
