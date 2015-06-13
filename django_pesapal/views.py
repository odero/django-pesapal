
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic.base import View, RedirectView, TemplateView

from xml.etree import cElementTree as ET

import conf as settings

import logging
import oauth2 as oauth
import requests
import urllib

DEFAULT_TYPE = "MERCHANT"
Transaction = get_model(settings.PESAPAL_TRANSACTION_MODEL)

logger = logging.getLogger(__name__)


class PaymentRequestMixin(object):

    def sign_request(self, params, url_to_sign):
        token = None

        # Default signature method is SignatureMethod_HMAC_SHA1
        signature_method = getattr(oauth, settings.PESAPAL_OAUTH_SIGNATURE_METHOD)()

        consumer = oauth.Consumer(settings.PESAPAL_CONSUMER_KEY, settings.PESAPAL_CONSUMER_SECRET)
        signed_request = oauth.Request.from_consumer_and_token(consumer, http_url=url_to_sign, parameters=params, is_form_encoded=True)
        signed_request.sign_request(signature_method, consumer, token)
        return signed_request

    def build_signed_request(self, payload):
        '''
        Returns a signed OAuth request. Assumes http protocol if request parameter is not provided.
        Otherwise it tries to figure out the url using the request object.
        '''

        if self.request:
            callback_url = self.request.build_absolute_uri(reverse(settings.PESAPAL_OAUTH_CALLBACK_URL))
        else:
            current_site = Site.objects.get_current()
            protocol = 'http' if settings.PESAPAL_DEMO else 'https'
            callback_url = '{0}://{1}{2}'.format(protocol, current_site.domain, reverse(settings.PESAPAL_OAUTH_CALLBACK_URL))

        params = {
            'oauth_callback': callback_url,
            'pesapal_request_data': payload,
        }

        signed_request = self.sign_request(params, settings.PESAPAL_IFRAME_LINK)

        return signed_request

    def generate_payload(self, **kwargs):
        '''
        Generates the XML payload required by Pesapal
        '''
        defaults = {
            'amount': 0,
            'description': '',
            'reference': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'type': DEFAULT_TYPE,
        }

        defaults.update(kwargs)

        xml_doc = ET.Element('PesapalDirectOrderInfo')
        xml_doc.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml_doc.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        xml_doc.set('xmlns', 'http://www.pesapal.com')

        for k, v in defaults.items():
            # convert keys into pesapal properties format e.g. first_name --> FirstName
            key_items = [str(x).title() for x in k.split('_')]
            k = ''.join(key_items)
            xml_doc.set(k, str(v))

        pesapal_request_data = ET.tostring(xml_doc)
        return pesapal_request_data

    def get_payment_url(self, **kwargs):
        '''
        Use the computed order information to generate a url for the Pesapal iframe.

        Params should include the following keys:
            Required params: `amount`, `description`, `reference`, `email`
            Optional params: `first_name`, `last_name`, `type`
        '''
        # assert type(params) == type({}), "Params must be of type 'dict'"

        # generate xml order
        payload = self.generate_payload(**kwargs)

        # generate iframe url
        signed_request = self.build_signed_request(payload)
        return signed_request.to_url()

    def get_payment_status(self, **kwargs):

        '''
        Query the payment status from pesapal using the `transaction_id` and the `merchant_reference_id`

        Params should include the following keys:
            Required params: `pesapal_merchant_reference`, `pesapal_transaction_tracking_id`
        '''

        params = {
            'pesapal_merchant_reference': '',
            'pesapal_transaction_tracking_id': '',
        }

        params.update(**kwargs)

        signed_request = self.sign_request(params, settings.PESAPAL_QUERY_STATUS_LINK)

        url = signed_request.to_url()

        response = requests.get(url, headers={'content-type': 'text/namevalue; charset=utf-8'})
        if response.status_code != requests.codes.ok:
            logger.error('Unable to complete payment status request with error response code {0}'.format(response.status_code))
            comm_status = False
        else:
            comm_status = True

        response_data = {}
        response_data['raw_request'] = url
        response_data['raw_response'] = response.text
        response_data['comm_success'] = comm_status

        _, values = response.text.split('=')
        _, payment_method, status, _ = values.split(',')
        response_data['payment_status'] = status
        response_data['payment_method'] = payment_method

        return response_data


class TransactionCompletedView(TemplateView):
    '''
    After Pesapal processes the transaction this will save the transaction and then redirect
    to whatever redirect URL in your settings as `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.

    For further processing just create a `post_save` signal on the `Transaction` model.
    '''

    template_name = 'django_pesapal/post_payment.html'

    def get(self, request, *args, **kwargs):

        transaction_id = request.GET.get('pesapal_transaction_tracking_id', 0)
        merchant_reference = request.GET.get('pesapal_merchant_reference', 0)

        if transaction_id and merchant_reference:
            self.transaction, created = Transaction.objects.get_or_create(
                merchant_reference=merchant_reference,
                pesapal_transaction=transaction_id
            )

        return super(TransactionCompletedView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        ctx = super(TransactionCompletedView, self).get_context_data(**kwargs)

        url_params = '?' + urllib.urlencode(
            {
                'pesapal_merchant_reference': self.transaction.merchant_reference,
                'pesapal_transaction_tracking_id': self.transaction.pesapal_transaction
            }
        )

        completed_url = reverse(settings.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL)
        completed_url += url_params
        ctx['transaction_completed_url'] = completed_url

        status_url = reverse('transaction_status')
        status_url += url_params

        ctx['check_status_url'] = status_url
        ctx['payment_status'] = self.transaction.payment_status

        if self.transaction.payment_status == Transaction.PENDING:
            message = _('Your payment is being processed. We will notify you once it has completed')
            ctx['payment_pending'] = True
        else:
            if self.transaction.payment_status == Transaction.COMPLETED:
                message = mark_safe(
                    _('''Your payment has been successfully processed.
                        The page should automatically redirect in <span class='countdown'>3</span> seconds.
                    ''')
                )
            elif self.transaction.payment_status == Transaction.FAILED:
                message = _('The processing of your payment failed. Please contact the system administrator.')
            else:
                # INVALID
                message = _('The transaction details provided were invalid.')

        ctx['message'] = message
        return ctx


class UpdatePaymentStatusMixin(PaymentRequestMixin):
    def get_params(self):
        self.merchant_reference = self.request.GET.get('pesapal_merchant_reference', 0)
        self.transaction_id = self.request.GET.get('pesapal_transaction_tracking_id', 0)

        params = {
            'pesapal_merchant_reference': self.merchant_reference,
            'pesapal_transaction_tracking_id': self.transaction_id,
        }

        return params

    def process_payment_status(self):
        params = self.get_params()

        self.transaction = get_object_or_404(
            Transaction,
            merchant_reference=self.merchant_reference,
            pesapal_transaction=self.transaction_id
        )

        # check status from pesapal server
        response = self.get_payment_status(**params)

        if response['payment_status'] == 'COMPLETED':
            self.transaction.payment_status = Transaction.COMPLETED
            self.transaction.payment_method = response['payment_method']
        elif response['payment_status'] == 'FAILED':
            self.transaction.payment_status = Transaction.FAILED
            self.transaction.payment_method = response['payment_method']
            logger.error('Failed Transaction: {}'.format(self.transaction))
        elif response['payment_status'] == 'INVALID':
            self.transaction.payment_status = Transaction.INVALID
            logger.error('Invalid Transaction: {}'.format(self.transaction))

        self.transaction.save()


class TransactionStatusView(UpdatePaymentStatusMixin, RedirectView):
    permanent = False
    url = None

    def get_redirect_url(self, *args, **kwargs):

        params = self.get_params()
        self.process_payment_status()

        # redirect back to Transaction completed view
        url = reverse('transaction_completed')
        url += '?' + urllib.urlencode(params)
        return url


class IPNCallbackView(UpdatePaymentStatusMixin, View):
    def get(self, request, *args, **kwargs):
        self.process_payment_status()
        return HttpResponse('OK')
