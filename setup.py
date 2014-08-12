import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pesapal',
    version='0.1.2',
    packages=[
        'django_pesapal'
    ],
    include_package_data=True,
    license='Beer-ware License',
    description='A django port for pesapal payment gateway.',
    long_description=README,
    url='https://github.com/odero/',
    author='odero',
    install_requires=[
        'Django>=1.5.4',
        'oauth2',
        # 'django-uuidfield>=0.5.0beta',
    ],
    # dependency_links=[
    #     "https://github.com/odero/django-uuidfield/archive/master.zip#egg=django-uuidfield==0.5.0beta",
    # ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Beer-ware License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)