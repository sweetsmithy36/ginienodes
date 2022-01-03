from __future__ import absolute_import, unicode_literals

import datetime
from decimal import Decimal
from time import sleep

import requests
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from coinginie.utils.function import emailInvoiceClient
from coinginie.wallet.models import Deposit, Transactions, Wallet
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
    sleep(2)
    emailInvoiceClient(to_email, subject, body)
    return None


@celery_app.task()
def send_admin_mail(to_email, subject, body):
    sleep(2)
    emailInvoiceClient(to_email, subject, body)
    return None




@celery_app.task()
def daily_roi(instance_id):
    instance = Deposit.objects.get(id=instance_id)
    profit = Decimal(instance.amount) * Decimal(instance.user.subscription.contract.profit)
    
    if instance.verified == True:
        Transactions.objects.create(
            user = instance.user,
            currency = instance.currency,
            type = Transactions.ROI,
            amount = profit,
            verified = True
        )
       
        if instance.currency == Deposit.BITCOIN:
            bal = instance.profit + instance.user.wallet.bitcoin_balance
            t_inv = instance.user.wallet.total_investment + profit
            Wallet.objects.filter(
                user=instance.user,
            ).update(bitcoin_balance=bal, recent_balance_added=profit, total_investment=t_inv)
        elif instance.currency == Deposit.LITECOIN:
            bal = profit + instance.user.wallet.litecoin_balance
            t_inv = instance.user.wallet.total_investment + profit
            Wallet.objects.filter(
                user=instance.user,
            ).update(litecoin_balance=bal, recent_balance_added=profit, total_investment=t_inv)
        elif instance.currency == Deposit.ETHEREUM:
            bal = profit + instance.user.wallet.ethereum_balance
            t_inv = instance.user.wallet.total_investment + profit
            Wallet.objects.filter(
                user=instance.user,
            ).update(ethereum_balance=bal, recent_balance_added=profit, total_investment=t_inv)
