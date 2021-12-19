import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from formtools.preview import FormPreview

from coinginie.contracts.models import Contract
from coinginie.users.forms import AccountSettingsForm, DocFileForm, InvestorForm
from coinginie.users.models import AccountSettings, Investor
from coinginie.wallet.forms import InvestForm, WithdrawForm
from coinginie.wallet.models import Deposit, Transactions, Wallet, Withdraw
from coinginie.wallet.tasks import send_admin_mail, send_deposit_mail

User = get_user_model()

today = datetime.date.today()


class WithdrawView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Withdraw
    # template_name = "dashboard/profile.html"
    form_class = WithdrawForm
    success_message = _("Withdrawal successfully made. Please wait for confirmation")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.verified = False
        form.save()
        to_email = form.user.email
        subject = "[GinieNodes] Withdrawal Requested"
        body = f"""
        Dear {form.user.first_name},
        
        Your request for the withdrawal of ${form.amount}
        is being processed. An email will be sent to you once it has been confirmed.
        
        Please nne patient
        
        Yours Truly
        Ginie Nodes
        """
        send_deposit_mail.delay(to_email, subject, body)
        
        
        admin_subject = "[Withdrawal Request] Admin Response"
        admin_body = f"""
        A withdrawal request has been made for {form.user.username}.
        
        Confirm the withdrawal request if they have been verified
        """
        admins = settings.ADMINS

        send_admin_mail.delay(admins, admin_subject, admin_body)
        return self.get_success_url()
    
class InvestView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Deposit
    # template_name = "dashboard/profile.html"
    form_class = InvestForm
    success_message = _("Investment successfully made. Please wait for confirmation")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.verified = False
        form.save()
        to_email = form.user.email
        subject = "[GinieNodes] Withdrawal Requested"
        body = f"""
        Dear {form.user.first_name},
        
        Your investment of ${form.amount} is being processed. 
        An email will be sent to you once it has been confirmed.
        
        Please nne patient
        
        Yours Truly
        Ginie Nodes
        """
        send_deposit_mail.delay(to_email, subject, body)

        admin_subject = "[Investment Request] Admin Response"
        admin_body = f"""
        An investment request has been made for {form.user.username}.
        
        Confirm the request if the amount has reflected in account
        """
        admins = settings.ADMINS

        send_admin_mail.delay(admins, admin_subject, admin_body)

        return self.get_success_url()
    
    
@login_required
def verify_deposit(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    deposit = get_object_or_404(Deposit, id=id)
    Deposit.objects.filter(id=deposit.id, verified=False).update(verified=True)
    
    user = deposit.user
    sub = deposit.user.subscription
    expires = today + datetime.timedelta(weeks=deposit.user.subscription.contract.duration_weeks)

    if deposit.verified == True:
        Contract.objects.filter(
            subscription = sub,
            active = False,
        ).update(active = True, expires = expires)
        Transactions.objects.filter(
            user = user,
            currency = deposit.currency,
            type = Transactions.INVEST,
            amount = deposit.amount,
        ).update(verified = True)
        if deposit.currency == Deposit.BITCOIN:
            bal = deposit.amount + deposit.user.wallet.bitcoin_balance
            t_inv = deposit.user.wallet.total_investment + deposit.user.wallet.bitcoin_balance
            Wallet.objects.filter(
                user=user,
            ).update(bitcoin_balance=bal, recent_balance_added=deposit.amount, total_investment=t_inv)
        elif deposit.currency == Deposit.LITECOIN:
            bal = deposit.amount + deposit.user.wallet.litecoin_balance
            t_inv = deposit.user.wallet.total_investment + deposit.user.wallet.litecoin_balance
            Wallet.objects.filter(
                user=user,
            ).update(litecoin_balance=bal, recent_balance_added=deposit.amount, total_investment=t_inv)
        elif deposit.currency == Deposit.ETHEREUM:
            bal = deposit.amount + deposit.user.wallet.ethereum_balance
            t_inv = deposit.user.wallet.total_investment + deposit.user.wallet.ethereum_balance
            Wallet.objects.filter(
                user=user,
            ).update(ethereum_balance=bal, recent_balance_added=deposit.amount, total_investment=t_inv)
    to_email = deposit.user.email
    subject = "[GinieNodes] Deposit Confirmed"
    body = f"""
    Dear {deposit.user.first_name},
    
    Your request to invest the sum of ${deposit.amount} has been processed. 
    
    Please nne patient
    
    Yours Truly
    Ginie Nodes
    """
    send_deposit_mail.delay(to_email, subject, body)

    admin_subject = "[Investment Verified] Admin Notice"
    admin_body = f"""
    The investment for {deposit.user.username} has been confirmed..
    """
    admins = settings.ADMINS

    send_admin_mail.delay(admins, admin_subject, admin_body)

    messages.info(request, "Successfully Verified Deposit")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def verify_withdraw(request, id):
    if not request.user.is_superuser:
        return redirect("dashboard")
    withdraw = get_object_or_404(Withdraw, id=id)
    Withdraw.objects.filter(id=withdraw.id, verified=False).update(verified=True)
    user = withdraw.user
    sub = withdraw.user.subscription
    expires = today + datetime.timedelta(weeks=withdraw.user.subscription.contract.duration_weeks)
    if withdraw and withdraw.verified == True and user.can_withdraw == True:
        if withdraw.currency == Withdraw.BITCOIN:
            bal = Decimal(withdraw.user.wallet.bitcoin_balance) - Decimal(withdraw.amount)
            Wallet.objects.filter(
                user=user,
            ).update(bitcoin_balance=bal, recent_balance_added=withdraw.amount)
        elif withdraw.currency == Withdraw.LITECOIN:
            bal = withdraw.user.wallet.litecoin_balance - withdraw.amount
            Wallet.objects.filter(
                user=user,
            ).update(litecoin_balance=bal, recent_balance_added=withdraw.amount)
        elif withdraw.currency == Withdraw.ETHEREUM:
            bal = withdraw.user.wallet.ethereum_balance - withdraw.amount
            Wallet.objects.filter(
                user=user,
            ).update(ethereum_balance=bal, recent_balance_added=withdraw.amount)

    to_email = withdraw.user.email
    subject = "[GinieNodes] Withdrawal Confirmed"
    body = f"""
    Dear {withdraw.user.first_name},
    
    Your request for the withdrawal of ${withdraw.amount} has been processed. 
    
    Please be patient
    
    Yours Truly
    Ginie Nodes
    """
    send_deposit_mail.delay(to_email, subject, body)

    admin_subject = "[Investment Verified] Admin Notice"
    admin_body = f"""
    The withdrawal request for {withdraw.user.username} has been confirmed..
    """
    admins = settings.ADMINS

    send_admin_mail.delay(admins, admin_subject, admin_body)

    messages.info(request, "Successfully verified withdrawal")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def all_transactions(request):
    deposits = Deposit.objects.all()
    withdrawals = Withdraw.objects.all()
    return render(request, 'users/admin.html', {"objects":deposits, "withdrawals":withdrawals})
