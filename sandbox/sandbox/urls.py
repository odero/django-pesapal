
try:
    from django.urls import include, re_path as url
except ImportError:
    # support django<4.0
    from django.conf.urls import include, re_path as url

from django.contrib import admin

from testapp.views import PaymentView, PaymentViewV3

admin.autodiscover()

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", PaymentView.as_view(), name="payment"),
    url(r"^v3/$", PaymentViewV3.as_view(), name="paymentv3"),
    url(r"^", include("django_pesapal.urls")),
    url(r"^v3/", include("django_pesapalv3.urls")),
]
