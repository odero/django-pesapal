=============================
django-pesapal
=============================

.. image:: https://badge.fury.io/py/django-pesapal.png
    :target: https://badge.fury.io/py/django-pesapal

.. image:: https://travis-ci.org/odero/django-pesapal.png?branch=master
    :target: https://travis-ci.org/odero/django-pesapal

.. image:: https://coveralls.io/repos/odero/django-pesapal/badge.png?branch=master
    :target: https://coveralls.io/r/odero/django-pesapal?branch=master

A django port of pesapal payment gateway

Documentation
-------------

The full documentation is at https://django-pesapal.readthedocs.org.

Quickstart
----------

Install django-pesapal::

    pip install django-pesapal

Then use it in a project::

    import django_pesapal


Note: You'll need to install this fork of `django-uuidfield` first::

    pip install git+git://github.com/odero/django-uuidfield.git#egg=django-uuidfield

For some reason, adding dependncy_links in `setup.py` just isn't working out for me.
If you can get that working send me a pull request.

#. Add `django_pesapal` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
        ...
        'django_pesapal',
    )

#. Include the `django_pesapal` URLconf in your project urls.py like this::

    url(r'^payments/', include('django_pesapal.urls')),

This is optional. You can set your own return url by adding this to `settings.py`::

    PESAPAL_OAUTH_CALLBACK_URL = 'app_name:url_name'  # this needs to be a reversible

#. Run `python manage.py syncdb` to create the polls models.

#. Create a method that receives payment details and returns the pesapal iframe url::

    from django_pesapal.app import get_payment_url

    def get_pesapal_payment_iframe():
        '''
        Authenticates with pesapal to get the payment iframe src
        '''

        order_info = {
            'amount': 100,
            'description': 'Payment for X',
            'reference': 2,  # some object id
            'email': 'user@example.com'
        }

        iframe_src_url = get_payment_url(**order_info)
        return iframe_src_url


**NB:**

`get_payment_url` is defined as::

    def get_payment_url(**kwargs):
        '''
        Use the computed order information to generate a url for the Pesapal iframe.

        Params should include the following keys:
            Required params: `amount`, `description`, `reference`, `email`
            Optional params: `first_name`, `last_name`
        '''

        `get_payment_url` is defined as::


`get_payment_status` is used get the payment status and is defined as::

    def get_payment_status(**kwargs):

        '''
        Query the payment status from pesapal using the transaction id and the merchant reference id

        Params should include the following keys:
            Required params: `pesapal_merchant_reference`, `pesapal_transaction_tracking_id`
        '''


It returns a dictionary with the following keys

    response_data['_raw_request']    The params that the request were made with
    response_data['_raw_response']   Useful for debugging
    response_data['_comm_success']   A bool communication status
    response_data['_payment_status'] The payment status
    response_data['_response_time']  Time taken for the response

`get_transaction_model` method is used to to obtain the transaction model set in the settings file
 with the key PESAPAL_TRANSACTION_MODEL with the following format app_label.model_name.
 The set model is to extend the
 django_pesapal BaseTransaction model with your additional custom fields.

Configuration
=============

+---------------------------------------------------+--------------------------------------------------------+
| Setting                                           | Default Value                                          |
+===================================================+========================================================+
| PESAPAL_DEMO                                      | True                                                   |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_CONSUMER_KEY                              | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_CONSUMER_SECRET                           | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_IFRAME_LINK (if PESAPAL_DEMO=True)        | 'http://demo.pesapal.com/api/PostPesapalDirectOrderV4' |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_IFRAME_LINK (if PESAPAL_DEMO=False)       | 'https://www.pesapal.com/api/PostPesapalDirectOrderV4' |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_QUERY_STATUS_LINK (if PESAPAL_DEMO=True)  | 'http://demo.pesapal.com/API/QueryPaymentStatus'       |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_QUERY_STATUS_LINK (if PESAPAL_DEMO=False) | 'https://www.pesapal.com/API/QueryPaymentStatus'       |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_CALLBACK_URL                        | 'transaction_completed'                                |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_SIGNATURE_METHOD                    | 'SignatureMethod_HMAC_SHA1'                            |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL          | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_ITEM_DESCRIPTION                          | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_MODEL                         | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_FAILED_REDIRECT_URL           | ''                                                     |
+---------------------------------------------------+--------------------------------------------------------+

The sandbox project in the repo can be used as a rough guide to using this api implementation.