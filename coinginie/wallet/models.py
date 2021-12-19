from __future__ import absolute_import, unicode_literals

import datetime
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
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from coinginie.contracts.models import Contract

today = datetime.date.today()
from django.contrib.auth.decorators import login_required

MALE = "Male"
FEMALE = "Female"
OTHERS = "Others"
GENDER = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHERS, "Others"),
)
MARRIED = "Married"
SINGLE = "Single"
DIVORCED = "Divorced"
SEPERATED = "Seperated"
MARITAL = (
    (MARRIED, "Married"),
    (SINGLE, "Single"),
    (DIVORCED, "Divorced"),
    (SEPERATED, "Seperated"),
)
FATHER = "Father"
MOTHER = "Mother"
UNCLE = "Uncle"
AUNTY = "Aunty"
BROTHER = "Brother"
SISTER = "Sister"
OTHER = "Other"
RELATIONSHIP = (
    (FATHER, "Father"),
    (MOTHER, "Mother"),
    (UNCLE, "Uncle"),
    (AUNTY, "Aunty"),
    (BROTHER, "Brother"),
    (SISTER, "Sister"),
    (OTHER, "Other"),
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def user_dp(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "dp/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )
    


SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"

class ExchangeRate(TimeStampedModel):
    bitcoin_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    litecoin_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    ethereum_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return "Current Exchange Rates"

    class Meta:
        managed = True
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        ordering = ["-created"]
        

class Wallet(TimeStampedModel):
    user = OneToOneField("users.User", on_delete=CASCADE, related_name="wallet")
    exh_rate = ForeignKey(ExchangeRate, on_delete=CASCADE, related_name="exchrate", default=1)
    
    bitcoin_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    litecoin_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    ethereum_balance = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    recent_balance_added = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    total_investment = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    # total_withdrawals = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    @property
    def total_balance(self):
        bal = self.bitcoin_balance + self.litecoin_balance + self.ethereum_balance
        return bal
    
    def btc(self):
        return self.bitcoin_balance / self.exh_rate.bitcoin_balance 

    def eth(self):
        return self.ethereum_balance / self.exh_rate.ethereum_balance 

    def ltc(self):
        return self.litecoin_balance / self.exh_rate.litecoin_balance 
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Wallet Balance"

    class Meta:
        managed = True
        verbose_name = "Wallet Balance"
        verbose_name_plural = "Wallet Balances"
        ordering = ["-created"]

class Withdraw(TimeStampedModel):
    BITCOIN = "BITCOIN"
    ETHEREUM = "ETHEREUM"
    LITECOIN = "LITECOIN"
    CURRENCY = (
        (BITCOIN,"Bitcon"),
        (ETHEREUM,"Ethereum"),
        (LITECOIN,"Litecoin"),
    )
    user = ForeignKey("users.User", on_delete=CASCADE, related_name="withdraw")
    exh_rate = ForeignKey(ExchangeRate, on_delete=CASCADE, related_name="deprate", default=1)
    currency = CharField(max_length=60, choices=CURRENCY, default=BITCOIN, blank=True)
    address = CharField(max_length=250)
    amount = DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    verified = BooleanField(default=False)

    def btc(self):
        return self.amount / self.exh_rate.bitcoin_balance 

    def eth(self):
        return self.amount / self.exh_rate.ethereum_balance 

    def ltc(self):
        return self.amount / self.exh_rate.litecoin_balance 

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Withdrawal"

    class Meta:
        managed = True
        verbose_name = "Withdrawal"
        verbose_name_plural = "Withdrawals"
        ordering = ["-created"]

class Deposit(TimeStampedModel):
    BITCOIN = "BITCOIN"
    ETHEREUM = "ETHEREUM"
    LITECOIN = "LITECOIN"
    CURRENCY = (
        (BITCOIN,"Bitcon"),
        (ETHEREUM,"Ethereum"),
        (LITECOIN,"Litecoin"),
    )
    user = ForeignKey("users.User", on_delete=CASCADE, related_name="invest")
    exh_rate = ForeignKey(ExchangeRate, on_delete=CASCADE, related_name="invrate", default=1)
    currency = CharField(max_length=60, choices=CURRENCY, default=BITCOIN, blank=True)
    amount = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    verified = BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Deposit"

    def btc(self):
        return self.amount / self.exh_rate.bitcoin_balance 

    def eth(self):
        return self.amount / self.exh_rate.ethereum_balance 

    def ltc(self):
        return self.amount / self.exh_rate.litecoin_balance 

    class Meta:
        managed = True
        verbose_name = "Deposit"
        verbose_name_plural = "Deposits"
        ordering = ["-created"]

class Transactions(TimeStampedModel):
    BITCOIN = "BITCOIN"
    ETHEREUM = "ETHEREUM"
    LITECOIN = "LITECOIN"
    CURRENCY = (
        (BITCOIN,"Bitcon"),
        (ETHEREUM,"Ethereum"),
        (LITECOIN,"Litecoin"),
    )
    INVEST = "Invest"
    WITHDRAW = "Withdraw"
    TYPE = (
        (INVEST, "Invest"),
        (WITHDRAW, "Withdraw")
    )
    user = ForeignKey("users.User", on_delete=CASCADE, related_name="transaction")
    exh_rate = ForeignKey(ExchangeRate, on_delete=CASCADE, related_name="tranrate", default=1)
    currency = CharField(max_length=60, choices=CURRENCY, default=BITCOIN, blank=True)
    type = CharField(max_length=60, choices=TYPE, blank=True)
    amount = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    verified = BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} Transaction"

    def btc(self):
        return self.amount / self.exh_rate.bitcoin_balance 

    def eth(self):
        return self.amount / self.exh_rate.ethereum_balance 

    def ltc(self):
        return self.amount / self.exh_rate.litecoin_balance 

    class Meta:
        managed = True
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created"]
























