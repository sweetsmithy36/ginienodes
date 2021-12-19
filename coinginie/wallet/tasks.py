from __future__ import absolute_import, unicode_literals

import datetime
from time import sleep

import requests
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from coinginie.utils.function import emailInvoiceClient
from config import celery_app
from logger import LOGGER

User = get_user_model()
today = datetime.date.today()
now = timezone.now()

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@celery_app.task()
def send_deposit_mail(to_email, subject, body):
    sleep(10)
    emailInvoiceClient(to_email, subject, body)
    return None


@celery_app.task()
def send_admin_mail(to_email, subject, body):
    sleep(2)
    emailInvoiceClient(to_email, subject, body)
    return None
