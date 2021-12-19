from django.contrib import admin

from .models import Deposit, ExchangeRate, Transactions, Wallet, Withdraw

# Register your models here.
admin.site.register(Deposit)
admin.site.register(ExchangeRate)
admin.site.register(Transactions)
admin.site.register(Wallet)
admin.site.register(Withdraw)

