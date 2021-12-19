import json
from datetime import timezone
from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from coinginie.wallet.models import ExchangeRate
# from requests_html import HTMLSession
from logger import LOGGER

User = get_user_model()


class Command(BaseCommand):
    help = _("Collect current bank rates")
    """
    BTC=189
    ETH=195
    LTC=191
    """

    def handle(self, *args, **kwargs):
        url = "https://investing-cryptocurrency-markets.p.rapidapi.com/currencies/get-rate"

        headers = {
            'x-rapidapi-host': "investing-cryptocurrency-markets.p.rapidapi.com",
            'x-rapidapi-key': "d2ee03b153msh7f9f91df901fa08p163f4ajsn694bb6dda556"
        }
        datum = {"fromCurrency":"189","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        x = requests.request("GET", url, params=datum, headers=headers)
        if x.status_code != 200:
            return str(x.status_code)
        eth = {"fromCurrency":"195","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        xe = requests.request("GET", url, params=eth, headers=headers)
        if xe.status_code != 200:
            return str(xe.status_code)
        ltc = {"fromCurrency":"191","toCurrency":"12","lang_ID":"1","time_utc_offset":"28800"}
        xl = requests.request("GET", url, params=ltc, headers=headers)
        if xl.status_code != 200:
            return str(xl.status_code)

        results = x.json()
        resultseth = xe.json()
        resultsltc = xl.json()
        usd = Decimal(results["data"][0][0]["basic"])
        eusd = Decimal(resultseth["data"][0][0]["basic"])
        lusd = Decimal(resultsltc["data"][0][0]["basic"])
        ExchangeRate.objects.create(bitcoin_balance=usd, litecoin_balance=lusd,  ethereum_balance=eusd)
        self.stdout.write("Exchange Rate Retrieved Successfully.")
