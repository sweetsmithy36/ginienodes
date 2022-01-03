from __future__ import absolute_import, unicode_literals

import datetime
from time import sleep

import requests
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from coinginie.contracts.models import Subscription
from coinginie.utils.function import emailInvoiceClient
from coinginie.wallet.models import Deposit, Transactions, Wallet
from config import celery_app
from logger import LOGGER

User = get_user_model()
today = datetime.date.today()
now = timezone.now()




