
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import View, RedirectView, TemplateView

from xml.etree import cElementTree as ET

from models import Transaction

import conf as settings

import logging
import oauth2 as oauth
import requests
import time
import urllib

DEFAULT_TYPE = "MERCHANT"

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
        response_data['comm_success'] = comm_status  # communication status
        response_data['payment_status'] = response.text.split('=')[1]  # The important detail

        return response_data


class TransactionCompletedView(TemplateView):
    template_name = 'django_pesapal/post_payment.html'

    def get(self, request, *args, **kwargs):
        '''
        After Pesapal processes the transaction this will save the transaction and then redirect
        to whatever reidrect URL in your settings as `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.

        For further processing just create a `post_save` signal on the `Transaction` model.
        '''
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

        completed_url = reverse(settings.PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL)
        ctx['transaction_completed_url'] = completed_url

        status_url = reverse('transaction_status')
        status_url += '?' + urllib.urlencode({
                'pesapal_merchant_reference': self.transaction.merchant_reference,
                'pesapal_transaction_tracking_id': self.transaction.pesapal_transaction
            }
        )

        ctx['check_status_url'] = status_url

        if self.transaction.payment_status == Transaction.PENDING:
            message = _('Your payment is being processed. We will notify you once it has completed')
            ctx['payment_pending'] = True
        else:
            if self.transaction.payment_status == Transaction.COMPLETED:
                message = _('Your payment has been successfully processed. The page should automatically redirect in 3 seconds.')
            elif self.transaction.payment_status == Transaction.FAILED:
                message = _('The processing of your payment failed. Please contact the system administrator.')
            else:
                # INVALID
                message = _('The payment details you provided are invalid. Please confirm they are correct and then try again in 5 minutes.')

        ctx['message'] = message
        return ctx
class TransactionStatusView(RedirectView, PaymentRequestMixin):
    permanent = False
    url = None

    def get_redirect_url(self, *args, **kwargs):
        merchant_reference = self.request.GET.get('pesapal_merchant_reference', 0)
        transaction_id = self.request.GET.get('pesapal_transaction_tracking_id', 0)

        params = {
            'pesapal_merchant_reference': merchant_reference,
            'pesapal_transaction_tracking_id': transaction_id,
        }

        transaction = get_object_or_404(
            Transaction,
            merchant_reference=merchant_reference,
            pesapal_transaction=transaction_id
        )

        # check status from pesapal server
        response = self.get_payment_status(**params)

        if response['payment_status'] == 'COMPLETED':
            transaction.payment_status = Transaction.COMPLETED
        elif response['payment_status'] == 'FAILED':
            transaction.payment_status = Transaction.FAILED
            logger.error('Failed Transaction: {}'.format(transaction))
        elif response['payment_status'] == 'INVALID':
            transaction.payment_status = Transaction.INVALID
            logger.error('Invalid Transaction: {}'.format(transaction))

        transaction.save()

        # redirect back to Transaction completed view
        url = reverse('transaction_completed')
        url += '?' + urllib.urlencode(params)
        return url
