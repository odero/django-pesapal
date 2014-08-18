#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_pesapal

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_pesapal.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-pesapal',
    version=version,
    description="""A django port of pesapal payment gateway""",
    long_description=readme + '\n\n' + history,
    author='Billy Odero',
    url='https://github.com/odero/django-pesapal',
    packages=[
        'django_pesapal',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.5.4',
        'oauth2',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-pesapal',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)