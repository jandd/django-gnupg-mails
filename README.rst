Created by `Jan Dittberner <http://twitter.com/jandd>`_

Introduction
============

django-gnupg-mails provides a class gnupg_mails.message.GnuPGMessage that
extends Django's django.core.mail.EmailMessage with the functionality to send
PGP/MIME signed emails.

  * Documentation: http://django-gnupg-mails.readthedocs.org/
  * Source: https://github.com/jandd/django-gnupg-mails


Dependencies
============

  * `gnupg <https://pypi.python.org/pypi/python-gnupg>`_ is required for
    signing the mails


Installation
============

The easiest way to install django-gnupg-mails is directly from PyPI using `pip
<http://www.pip-installer.org/>`_ by running the command below::

    $ pip install -U django-gnupg-mails

Otherwise you can download django-gnupg-mails and install it directly from
source::

    $ python setup.py install


Usage
=====

Define settings.GNUPG_HOMEDIR to point to a GnuPG home directory containing a
private key with signing capabilities.

Instead of using Django's EmailMessage you can just use
gnupg_mails.message.GnuPGMessage. The class is a drop-in replacement and can
used in the same way as the original class as documented in `The Django
documentation
<https://docs.djangoproject.com/en/dev/topics/email/#the-emailmessage-class>`_.


Similar packages
================

You may want to have a look at `django-email-extras
<https://github.com/stephenmcd/django-email-extras>`_ by Stephen McDonald for
other GnuPG related functionality. Stephen's package allows sending PGP
encrypted mail and provides a nice email test backend.
