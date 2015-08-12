==============
django-pesapal
==============

.. image:: https://badge.fury.io/py/django-pesapal.png
   :target: https://badge.fury.io/py/django-pesapal

.. image:: https://travis-ci.org/odero/django-pesapal.png?branch=master
   :target: https://travis-ci.org/odero/django-pesapal

.. image:: https://coveralls.io/repos/odero/django-pesapal/badge.png?branch=master
   :target: https://coveralls.io/r/odero/django-pesapal?branch=master

.. image:: https://pypip.in/status/django-pesapal/badge.svg
   :target: https://pypi.python.org/pypi/django-pesapal/
   :alt: Development Status

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

#. Add `django_pesapal` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
        ...
        'django_pesapal',
    )

#. Include the `django_pesapal` URLconf in your project urls.py like this::

    url(r'^payments/', include('django_pesapal.urls')),

#. You can set your own return url by adding this to `settings.py`::

    PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = 'app_name:url_name'  # this needs to be a reversible

#. Run `python manage.py migrate` to create the models.

#. Create a method that receives payment details and returns the pesapal iframe url::

    from django_pesapal.views import PaymentRequestMixin

    class PaymentView(PaymentRequestMixin):

        def get_pesapal_payment_iframe(self):

            '''
            Authenticates with pesapal to get the payment iframe src
            '''
            order_info = {
                'first_name': 'Some',
                'last_name': 'User',
                'amount': 100,
                'description': 'Payment for X',
                'reference': 2,  # some object id
                'email': 'user@example.com',
            }

            iframe_src_url = self.get_payment_url(**order_info)
            return iframe_src_url

#. Once payment has been processed, you will be redirected to an intermediate screen where the user can finish ordering. Clicking the "Finish Ordering" button will check the payment status to ensure that the payment was successful and then redirects the user to `PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL`.


Configuration
-------------

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
| PESAPAL_QUERY_STATUS_LINK (Demo Mode=True)  | 'http://demo.pesapal.com/API/QueryPaymentDetails'      |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_QUERY_STATUS_LINK (Demo Mode=False) | 'https://www.pesapal.com/API/QueryPaymentDetails'      |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_CALLBACK_URL                  | 'transaction_completed'                                |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_OAUTH_SIGNATURE_METHOD              | 'SignatureMethod_HMAC_SHA1'                            |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL    | '/'                                                    |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_FAILED_REDIRECT_URL     | ''                                                     |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_REDIRECT_WITH_REFERENCE             | True                                                   |
+---------------------------------------------+--------------------------------------------------------+
| PESAPAL_TRANSACTION_MODEL                   | 'django_pesapal.Transaction'                           |
+---------------------------------------------+--------------------------------------------------------+
