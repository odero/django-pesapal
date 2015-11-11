.. :changelog:

History
-------
1.0.0 (2015-11-11)
++++++++++++++++++
- Support Django 1.8
- Support Py33 and Py34
- Return proper IPN response

0.3.4 (2015-08-12)
++++++++++++++++++
- Restructure flow to better support IPN processing

0.3.3 (2015-06-29)
++++++++++++++++++
- Setup build had not packaged the templates

0.3.2 (2015-06-13)
++++++++++++++++++
- Fix documentation formatting issues

0.3.1 (2015-06-13)
++++++++++++++++++
- Allow specifying own transaction model
- Pass all transaction info when redirecting
- Update intermediate template

0.3 (2015-06-12)
++++++++++++++++++
- Introduce intermediate payment processing screen
- Update Django version to 1.7+
- Add support to receive and process IPN
- Save all details about the transaction and status

0.2.1 (2015-04-03)
++++++++++++++++++
- Added test sandbox
- Updated Django version
- Updated django-uuidfield

0.2 (2015-03-17)
++++++++++++++++++
- Support anonymous checkouts
- Add support for getting payment status
- Major structural refactoring. Use mixins
- Use Mixins and XML Builder

0.1.5 (2014-09-25)
++++++++++++++++++
- Pin dependencies to specific versions
- Update how imports should be done
- Remove imports from __init__.py

0.1.4 (2014-09-23)
++++++++++++++++++
- Fix import bug. Tests for projects using this fail in Shippable
- Set max Django version to 1.7

0.1.3 (2014-07-18)
++++++++++++++++++
- Packaging for PyPi

0.1.2 (2014-06-30)
++++++++++++++++++
- Fix import bug in urls.py
- Fix how callback url is constructed
- Fix: Live URL uses https

0.1.1 (2014-06-30)
++++++++++++++++++
- Refactor handling of redirect urls. Model validation of transaction and merchant reference
- Rename settings to conf. Set default oauth redirect url
- Add django-uuidfield to dependencies

0.1.0 (2014-06-30)
++++++++++++++++++

* First release on PyPI.