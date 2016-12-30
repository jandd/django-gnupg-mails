from email.charset import Charset, QP
from email.encoders import encode_noop
from email.mime.application import MIMEApplication
from email.mime.nonmultipart import MIMENonMultipart
from email.utils import formatdate

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import SafeMIMEMultipart
from django.core.mail.message import MIMEMixin
from django.core.mail.message import make_msgid

from gnupg import GPG


class MIMEUTF8QPText(MIMEMixin, MIMENonMultipart):
    def __init__(self, payload, charset='utf-8'):
        MIMENonMultipart.__init__(self, 'text', 'plain', charset=charset)

        utf8qp = Charset(charset)
        utf8qp.body_encoding = QP
        self.set_payload(payload, charset=utf8qp)


class GnuPGMessage(EmailMessage):
    def __init__(self, *args, **kwargs):
        super(GnuPGMessage, self).__init__(*args, **kwargs)
        self.gpg = GPG(gnupghome=settings.GNUPG_HOMEDIR)

    def _normalize(self, original):
        return "\r\n".join(str(original).splitlines()[1:]) + "\r\n"

    def _sign(self, original):
        sig = self.gpg.sign(
            self._normalize(original), detach=True, clearsign=False)
        signature = MIMEApplication(
            str(sig), 'pgp-signature', encode_noop, name='signature.asc')
        signature.add_header('Content-Description', 'Digital signature')
        del signature['MIME-Version']
        return signature

    def message(self):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        msg = MIMEUTF8QPText(self.body, encoding)
        msg = self._create_message(msg)

        msg['Subject'] = self.subject
        msg['From'] = self.extra_headers.get('From', self.from_email)
        msg['To'] = self.extra_headers.get('To', ', '.join(self.to))
        if self.cc:
            msg['Cc'] = ', '.join(self.cc)

        header_names = [key.lower() for key in self.extra_headers]
        if 'date' not in header_names:
            msg['Date'] = formatdate()
        if 'message-id' not in header_names:
            msg['Message-ID'] = make_msgid()
        for name, value in self.extra_headers.items():
            if name.lower() in ('from', 'to'):
                # From and To are already handled
                continue
            msg[name] = value

        del msg['MIME-Version']

        wrapper = SafeMIMEMultipart(
            'signed', protocol='application/pgp-signature',
            micalg='pgp-sha512')
        wrapper.preamble = (
            "This is an OpenPGP/MIME signed message (RFC 4880 and 3156)"
        )

        # copy headers from original message to PGP/MIME envelope
        for header in msg.keys():
            if header.lower() not in (
                    'content-disposition', 'content-type', 'mime-version'
            ):
                for value in msg.get_all(header):
                    wrapper.add_header(header, value)
                del msg[header]

        for part in msg.walk():
            del part['MIME-Version']

        signature = self._sign(msg)

        wrapper['Content-Disposition'] = 'inline'
        wrapper.attach(msg)
        wrapper.attach(signature)

        return wrapper
