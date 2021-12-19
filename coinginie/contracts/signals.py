from __future__ import absolute_import, unicode_literals

import datetime

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from coinginie.contracts.models import Contract

from .models import Contract, Plans, Subscription

User = get_user_model()

today = datetime.date.today()

@receiver(post_save, sender=Subscription)
def contract_initiation_signal(sender, created, instance, *args, **kwargs):
    expires = today + datetime.timedelta(weeks=instance.contract.duration_weeks)
    if created:
        Contract.objects.create(
            subscription = instance,
            active = False
        )


@receiver(post_save, sender=Contract)
def contract_initiation_signal(sender, created, instance, *args, **kwargs):
    if created and instance.active == True and today >= instance.expires:
        Contract.objects.filter(
            subscription = instance.subscription,
            active = True
        ).update(active=False)
        User.objects.filter(username=instance.subscrition.user.username).update(can_withdraw=True)
