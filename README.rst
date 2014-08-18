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

    from django_pesapal import get_payment_url

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


**NB:** `get_payment_url` is defined as::

    def get_payment_url(**kwargs):
        '''
        Use the computed order information to generate a url for the Pesapal iframe.

        Params should include the following keys:
            Required params: `amount`, `description`, `reference`, `email`
            Optional params: `first_name`, `last_name`
        '''

Configuration
=============

+---------------------------------------------+--------------------------------------------------------+
| Setting                                     | Default Value                                          |
+=============================================+========================================================+
| PESAPAL_DEMO                                | True                                                   |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_CONSUMER_KEY                        | ''                                                     |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_CONSUMER_SECRET                     | ''                                                     |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_IFRAME_LINK (if PESAPAL_DEMO=True)  | 'http://demo.pesapal.com/api/PostPesapalDirectOrderV4' |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_IFRAME_LINK (if PESAPAL_DEMO=False) | 'https://www.pesapal.com/api/PostPesapalDirectOrderV4' |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_CALLBACK_URL                  | 'transaction_completed'                                |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_SIGNATURE_METHOD              | 'SignatureMethod_HMAC_SHA1'                            |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL    | ''                                                     |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_FAILED_REDIRECT_URL     | ''                                                     |
+---------------------------------------------+--------------------------------------------------------+
