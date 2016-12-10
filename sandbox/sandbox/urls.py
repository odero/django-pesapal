from django.conf.urls import include, url

from django.contrib import admin
from testapp.views import PaymentView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PaymentView.as_view(), name='payment'),
    url(r'^', include('django_pesapal.urls')),
]
