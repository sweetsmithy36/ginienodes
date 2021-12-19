from allauth.account.forms import (
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
)
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import Deposit, Withdraw

User = get_user_model()


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = [
            "currency",
            "address",
            "amount",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['currency'].widget = forms.RadioSelect(attrs={'class': 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Address','id':'autocomplete_input'})
        self.fields['amount'].widget = forms.NumberInput(attrs={'class': 'form-control mb-1','placeholder':'Wallet Address'})

        
class InvestForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = [
            "currency",
            "amount",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['currency'].widget = forms.RadioSelect(attrs={'class': 'form-control'})
        self.fields['amount'].widget = forms.NumberInput(attrs={'class': 'form-control'})
