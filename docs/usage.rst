======
Usage
======

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

**NOTE:** You can override the intermediate (`post_payment.html`) processing template if you 
need to have a customized look.
