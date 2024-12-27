import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],
        ROOT_URLCONF="django_pesapal.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django_pesapal",
            "django_pesapalv3",
        ],
        SITE_ID=1,
        NOSE_ARGS=["-s"],
    )

    try:
        import django

        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ["django_pesapal.tests", "django_pesapal3.tests"]

    # Run tests
    test_runner = NoseTestSuiteRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == "__main__":
    run_tests(*sys.argv[1:])
