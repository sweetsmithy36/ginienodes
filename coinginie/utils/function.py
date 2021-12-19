from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage

sender = settings.EMAIL_HOST_USER
admins = settings.ADMINS
def emailInvoiceClient(to_email, subject, body):
    from_email = sender
    subject = subject
    body = body
    message = EmailMessage(subject, body, from_email, [to_email])
    return message.send()
