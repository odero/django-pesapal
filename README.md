django-pesapal
==============================

A django port for pesapal payment gateway


Quick start
-----------

Note: You'll need to install this fork of `django-uuidfield` first:

        pip install git+git://github.com/odero/django-uuidfield.git#egg=django-uuidfield

For some reason, adding dependncy_links in `setup.py` just isn't working out for me.
If you can get that working send me a pull request.

1. Add `django_pesapal` to your `INSTALLED_APPS` setting like this:


        INSTALLED_APPS = (
            ...
            'django_pesapal',
        )

2. Include the `django_pesapal` URLconf in your project urls.py like this:

        url(r'^payments/', include('django_pesapal.urls')),

This is optional. You can set your own return url by adding this to `settings.py`:

        PESAPAL_OAUTH_CALLBACK_URL = 'app_name:url_name'  # this needs to be a reversible

3. Run `python manage.py syncdb` to create the polls models.

4. Create a method that receives payment details and returns the pesapal iframe url:
    
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


**NB:** `get_payment_url` is defined as:

        def get_payment_url(**kwargs):
            '''
            Use the computed order information to generate a url for the Pesapal iframe.

            Params should include the following keys:
                Required params: `amount`, `description`, `reference`, `email`
                Optional params: `first_name`, `last_name`
            '''
