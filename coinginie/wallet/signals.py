from __future__ import absolute_import, unicode_literals

import datetime
from decimal import Decimal

from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from coinginie.contracts.models import Contract

from .models import Deposit, Transactions, Wallet, Withdraw

today = datetime.date.today()

@receiver(post_save, sender=Deposit)
def contract_initiation_signal(sender, created, instance, *args, **kwargs):
    user = instance.user
    sub = instance.user.subscription
    expires = today + datetime.timedelta(weeks=instance.user.subscription.contract.duration_weeks)
    if created and instance.verified == False:
        # instance.verified = False
        Transactions.objects.create(
            user = user,
            currency = instance.currency,
            type = Transactions.INVEST,
            amount = instance.amount
        )
        
    if instance.verified == True:
        Contract.objects.filter(
            subscription = sub,
            active = False,
        ).update(active = True, expires = expires)
        Transactions.objects.filter(
            user = user,
            currency = instance.currency,
            type = Transactions.INVEST,
            amount = instance.amount,
        ).update(verified = True)
        if instance.currency == Deposit.BITCOIN:
            bal = instance.amount + instance.user.wallet.bitcoin_balance
            t_inv = instance.user.wallet.total_investment + instance.user.wallet.bitcoin_balance
            Wallet.objects.filter(
                user=user,
            ).update(bitcoin_balance=bal, recent_balance_added=instance.amount, total_investment=t_inv)
        elif instance.currency == Deposit.LITECOIN:
            bal = instance.amount + instance.user.wallet.litecoin_balance
            t_inv = instance.user.wallet.total_investment + instance.user.wallet.litecoin_balance
            Wallet.objects.filter(
                user=user,
            ).update(litecoin_balance=bal, recent_balance_added=instance.amount, total_investment=t_inv)
        elif instance.currency == Deposit.ETHEREUM:
            bal = instance.amount + instance.user.wallet.ethereum_balance
            t_inv = instance.user.wallet.total_investment + instance.user.wallet.ethereum_balance
            Wallet.objects.filter(
                user=user,
            ).update(ethereum_balance=bal, recent_balance_added=instance.amount, total_investment=t_inv)



@receiver(post_save, sender=Withdraw)
def contract_initiation_signal(sender, created, instance, *args, **kwargs):
    user = instance.user
    if created:
        Transactions.objects.create(
            user = user,
            currency = instance.currency,
            type = Transactions.WITHDRAW,
            amount = instance.amount
        )
        
    if created and instance.verified == True and user.can_withdraw == True:
        if instance.currency == Withdraw.BITCOIN:
            bal = Decimal(instance.user.wallet.bitcoin_balance) - Decimal(instance.amount)
            Wallet.objects.filter(
                user=user,
            ).update(bitcoin_balance=bal, recent_balance_added=instance.amount)
        elif instance.currency == Withdraw.LITECOIN:
            bal = instance.user.wallet.litecoin_balance - instance.amount
            Wallet.objects.filter(
                user=user,
            ).update(litecoin_balance=bal, recent_balance_added=instance.amount)
        elif instance.currency == Withdraw.ETHEREUM:
            bal = instance.user.wallet.ethereum_balance - instance.amount
            Wallet.objects.filter(
                user=user,
            ).update(ethereum_balance=bal, recent_balance_added=instance.amount)


