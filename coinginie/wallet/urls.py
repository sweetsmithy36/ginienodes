from django.urls import path

from .views import (
    InvestView,
    WithdrawView,
    all_transactions,
    verify_deposit,
    verify_withdraw,
)

app_name = "wallet"
urlpatterns = [
    path("~transactions/", view=all_transactions, name="transactions"),
    path("~invest/confirm/<int:id>/", view=verify_deposit, name="invest_verify"),
    path("~invest/", view=InvestView.as_view(), name="invest"),
    path("~withdraw/confirm/<int:id>/", view=verify_withdraw, name="withdraw_verify"),
    path("~withdraw/", view=WithdrawView.as_view(), name="withdraw"),
]
