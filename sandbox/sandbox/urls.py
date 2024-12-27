from django.conf.urls import include, url
from django.contrib import admin

# from debug_toolbar.toolbar import debug_toolbar_urls
import debug_toolbar.urls as debug_toolbar_urls

from testapp.views import PaymentView, PaymentViewV3

admin.autodiscover()

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", PaymentView.as_view(), name="payment"),
    url(r"^v3/$", PaymentViewV3.as_view(), name="paymentv3"),
    url(r"^", include("django_pesapal.urls")),
    url(r"^__debug__/", include(debug_toolbar_urls)),
]
