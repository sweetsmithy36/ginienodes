from __future__ import absolute_import, unicode_literals

import datetime
import json
import os
import random
from datetime import date, timedelta
from decimal import Decimal

# from cities_light.models import Country
from dateutil import relativedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import IntegrityError, OperationalError, transaction
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ManyToManyField,
    OneToOneField,
    PositiveSmallIntegerField,
)
from django.db.models.fields import TextField
from django.db.models.fields.files import ImageField
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

today = datetime.date.today()
    
class Plans(TimeStampedModel):
    ICON = (
        ("bx-walk", "WALK"),
        ("bx-run", "RUN"),
        ("bx-cycling", "BICYCLE"),
        ("bx-car", "CAR"),
    )
    name = CharField(max_length=250)
    
    min_amount = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    max_amount = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    features = TextField()
    
    icon = CharField(max_length=250, null=True, choices=ICON)
    
    profit = DecimalField(max_digits=5, decimal_places=2, default=0.25)
    
    duration_weeks = PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-created"]

class Subscription(TimeStampedModel):
    contract = ForeignKey(Plans, default=1, on_delete=CASCADE, related_name="subscription")
    user = OneToOneField("users.User", on_delete=CASCADE, related_name="subscription")

    def __str__(self):
        return f"{self.contract.name} - {self.user.name}"

    class Meta:
        managed = True
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscribes"
        ordering = ["-created"]

class Contract(TimeStampedModel):
    subscription = OneToOneField(Subscription, on_delete=CASCADE, related_name="subcontract")
    expires = DateField(blank=True, null=True)
    active = BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subscription.user.first_name} {self.subscription.user.last_name} | {self.subscription.contract.name} Contract"
    
    class Meta:
        managed = True
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created"]
    
