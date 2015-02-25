
try:
    # This will load when settings have been configured
    from django.contrib.sites.models import Site
    from django.core.urlresolvers import reverse
except Exception, e:
    pass

import logging
import oauth2 as oauth
# from xml.etree.cElementTree import XML, Element
# import xml.etree.cElementTree as ctree
import cgi
import requests
import time


import conf as settings

DEFAULT_TYPE = "MERCHANT"

logger = logging.getLogger('django_pesapal')

def get_signed_request(request, payload):
    '''
    Returns a signed OAuth request. Assumes http protocol if request parameter is not provided.
    Otherwise it tries to figure out the url using the request object.
    '''
    token = None

    if request:
        callback_url = request.build_absolute_uri(reverse(settings.PESAPAL_OAUTH_CALLBACK_URL))
    else:
        current_site = Site.objects.get_current()
        protocol = 'http' if settings.PESAPAL_DEMO else 'https'
        callback_url = '{0}://{1}{2}'.format(protocol, current_site.domain, reverse(settings.PESAPAL_OAUTH_CALLBACK_URL))

    params = {
        'oauth_callback': callback_url,
        'pesapal_request_data': payload
    }

    # Default signature method is SignatureMethod_HMAC_SHA1
    signature_method = getattr(oauth, settings.PESAPAL_OAUTH_SIGNATURE_METHOD)()

    consumer = oauth.Consumer(settings.PESAPAL_CONSUMER_KEY, settings.PESAPAL_CONSUMER_SECRET)
    signed_request = oauth.Request.from_consumer_and_token(consumer, http_url=settings.PESAPAL_IFRAME_LINK, parameters=params, is_form_encoded=True)
    signed_request.sign_request(signature_method, consumer, token)

    return signed_request


def generate_payload(**kwargs):
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

    xml_payload = '''
    <PesapalDirectOrderInfo
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        Amount="{amount}"
        Description="{description}"
        Reference="{reference}"
        FirstName="{first_name}"
        LastName="{last_name}"
        Email="{email}"
        Type="{type}"
        xmlns="http://www.pesapal.com"
    />
    '''

    xml_payload = xml_payload.format(**defaults)

    # Remove whitespace
    xml_payload = " ".join(xml_payload.split())

    # TODO: Try to build the same with XML to cater for more fields
    # xml_doc = XML(xml_payload)
    # xml_doc.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    # xml_doc.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    # xml_doc.set('xmlns', 'http://www.pesapal.com')

    # for k,v in defaults.items():
    #     xml_doc.set(k, str(v))

    # pesapal_request_data = cgi.escape(ctree.tostring(xml_doc))
    pesapal_request_data = cgi.escape(xml_payload)
    return pesapal_request_data


def get_payment_url(request=None, **kwargs):
    '''
    Use the computed order information to generate a url for the Pesapal iframe.

    Params should include the following keys:
        Required params: `amount`, `description`, `reference`, `email`
        Optional params: `first_name`, `last_name`, `type`
    '''
    # assert type(params) == type({}), "Params must be of type 'dict'"

    # generate xml order
    # print 'kwargs', kwargs
    payload = generate_payload(**kwargs)

    # generate iframe url
    signed_request = get_signed_request(request, payload)
    return signed_request.to_url()


def get_payment_status(**kwargs):

    '''
    Query the payment status from pesapal using the transaction id and the merchant reference id

    Params should include the following keys:
        Required params: `pesapal_merchant_reference`, `pesapal_transaction_tracking_id`
    '''

    params = {
        'pesapal_merchant_reference': '',
        'pesapal_transaction_tracking_id': '',
    }

    params.update(**kwargs)

    signature_method = getattr(oauth, settings.PESAPAL_OAUTH_SIGNATURE_METHOD)()

    consumer = oauth.Consumer(settings.PESAPAL_CONSUMER_KEY, settings.PESAPAL_CONSUMER_SECRET)
    signed_request = oauth.Request.from_consumer_and_token(consumer, http_url=settings.PESAPAL_QUERY_STATUS_LINK, parameters=params, is_form_encoded=True)
    signed_request.sign_request(signature_method, consumer, token=None)

    url = signed_request.to_url()

    start_time = time.time()
    response = requests.get(url, headers={'content-type': 'text/namevalue; charset=utf-8'})
    if response.status_code != requests.codes.ok:
        logger.error("Unable to complete payment status request with error response code %s", response.status_code )
        comm_status = False
    else:
        comm_status = True

    response_data = {}

    # !!! Important handle the response if it is not 'OK'
    response_data['_raw_request'] = url
    response_data['_raw_response'] = response.text
    response_data['_comm_success'] = comm_status # communication status
    response_data['_payment_status'] = response.text.partition('=')[2] # The important detail
    response_data['_response_time'] = (time.time() - start_time) * 1000.0

    return response_data