
from . import settings

import oauth2 as oauth
# from xml.etree.cElementTree import XML, Element
# import xml.etree.cElementTree as ctree
import cgi
# import requests

DEFAULT_TYPE = "MERCHANT"


def get_signed_request(payload):
    '''
    Returns a signed OAuth request
    '''
    token = None

    params = {
        'oauth_callback': settings.PESAPAL_OAUTH_CALLBACK_URL,
        'pesapal_request_data': payload
    }

    # Default signature method is SignatureMethod_HMAC_SHA1
    signature_method = getattr(oauth, settings.PESAPAL_OAUTH_SIGNATURE_METHOD)()

    consumer = oauth.Consumer(settings.PESAPAL_CONSUMER_KEY, settings.PESAPAL_CONSUMER_SECRET)
    signed_request = oauth.Request.from_consumer_and_token(consumer, http_url=settings.PESAPAL_IFRAME_LINK, parameters=params, is_form_encoded=True)
    signed_request.sign_request(signature_method, consumer, token)
    # print signed_request.to_url()
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


def get_payment_url(**kwargs):
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
    signed_request = get_signed_request(payload)
    return signed_request.to_url()
