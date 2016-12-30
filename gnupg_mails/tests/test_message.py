import logging
import os
import sys
from email.utils import formatdate
from shutil import rmtree
from tempfile import mkstemp

import django
from django.conf import settings
from django.test import TestCase
from django.test.utils import get_runner
from gnupg import GPG

from gnupg_mails.message import GnuPGMessage

log = logging.getLogger(__name__)


class TestGnuPGMessage(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGnuPGMessage, cls).setUpClass()
        gpg = GPG(gnupghome=settings.GNUPG_HOMEDIR)
        key_input = gpg.gen_key_input()
        gpg.gen_key(key_input)

    def test_message_signing(self):
        message = GnuPGMessage(subject='Test', body='Test body').message()
        self._verify(message)

    def test_message_signing_with_cc(self):
        message = GnuPGMessage(
            subject='Test', body='Test body',
            to=['receiver@example.org'], cc=['test@example.org']).message()
        self._verify(message)

    def test_message_signing_with_extra_headers(self):
        message = GnuPGMessage(subject='Test', body='Test body')
        message.extra_headers['X-Miau'] = 'Moo'
        message.extra_headers['From'] = 'analien@example.org'
        message.extra_headers['Date'] = formatdate()
        message.extra_headers['Message-ID'] = 'mysecret_id <test@localhorst>'
        self._verify(message.message())

    def test_message_signing_with_attachment(self):
        message = GnuPGMessage(subject='Test', body='Test body')
        message.attach("test.txt", "text data", "text/plain")
        self._verify(message.message())

    def _verify(self, message):
        log.debug(str(message))
        datafile = mkstemp()[1]
        sigfile = datafile + ".asc"
        try:
            with open(datafile, 'w') as data:
                signed_part = message.get_payload(0)
                data.write(
                    "\r\n".join(str(signed_part).splitlines()[1:]) + "\r\n")
            with open(sigfile, 'w') as signature:
                signature_part = message.get_payload(1)
                signature.write(
                    "\r\n".join(str(signature_part).splitlines()[1:]) + "\r\n")
            gpg = GPG(gnupghome=settings.GNUPG_HOMEDIR)
            with open(sigfile, 'rb') as signature_data:
                verified = gpg.verify_file(
                    signature_data, data_filename=datafile)
                self.assertTrue(verified.valid)
        finally:
            os.unlink(datafile)
            os.unlink(sigfile)

    @classmethod
    def tearDownClass(cls):
        rmtree(settings.GNUPG_HOMEDIR)
        super(TestGnuPGMessage, cls).tearDownClass()


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'gnupg_mails.tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['gnupg_mails.tests'])
    sys.exit(bool(failures))
