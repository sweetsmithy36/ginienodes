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

from .models import AccountSettings, Investor, PrivacyPolicies

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }




class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control mb-2','placeholder':'Enter Username','id':'username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter Password','id':'password'})
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        
        
class UserRegistrationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm):
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'username',
            'consent',
        ]
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'First Name'})
        self.fields['middle_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Middle Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Last Name'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-1','placeholder':'Enter Email','id':'email'})
        self.fields['email'].label="Email"
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Enter Username','id':'username1'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-1','placeholder':'Enter Password','id':'password1'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-1','placeholder':'Enter Confirm Password','id':'password2'})
        self.fields['password2'].label="Confirm Password"
        self.fields['consent'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['consent'].label="Accept Terms and Privacy Agreement"

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = [
            "gender",
            "image",
            "address",
            "phone",
            "dob",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['dob'].widget = forms.DateInput(attrs={'class': 'form-control', "placeholder":"2021-12-31", "data-date-container":'#datepicker1', "data-provide":"datepicker"})
        self.fields['image'].label="Passport"
        self.fields['address'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Address','id':'autocomplete_input'})
        # self.fields['gender'].widget = forms.Select(attrs={"data-placeholder":"Gender", "class":"chosen-select"})
        # self.fields['country'].widget = forms.Select(attrs={"data-placeholder":"Select Country", "class":"chosen-select"})

class DocFileForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ['doc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['doc'].widget = forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple':'multiple'})
        self.fields['doc'].label="Drivers License / Passport"

class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = AccountSettings
        fields = [
            "account_name",
            "account_number",
            "bank_name",
            "routing_no",
            'swift_code',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['account_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-1','placeholder':'Account Name'})
        self.fields['account_number'].widget = forms.NumberInput(attrs={"placeholder":"Account Number", "class":"form-control"})
        self.fields['routing_no'].widget = forms.NumberInput(attrs={"placeholder":"Routing Number", "class":"form-control"})
        self.fields['swift_code'].widget = forms.NumberInput(attrs={"placeholder":"Swift Code", "class":"form-control"})
        # self.fields['bank_name'].widget = forms.Select(attrs={"data-placeholder":"Bank Name", "class":"chosen-select"})
        
class PrivacyPoliciesForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicies
        fields = [
            "cookies_and_tracking",
            "google_ads",
            "social_account_integration",
            "personal_information",
            "commercial_information",
            "identifiers",
            "internet_or_other_electronic_network_activity_information",
            "age_restriction",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['cookies_and_tracking'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['google_ads'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['social_account_integration'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['personal_information'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['commercial_information'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['identifiers'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['internet_or_other_electronic_network_activity_information'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        self.fields['age_restriction'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})


    
class PasswordChangeForm(ChangePasswordForm):
      def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter currunt password','id':'password3'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password4'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter confirm password','id':'password5'})
        self.fields['password2'].label="Confirm Password"
        
        
class PasswordResetForm(ResetPasswordForm):
      def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2','placeholder':' Enter Email','id':'email1'})
        self.fields['email'].label="Email"
        
        
class PasswordResetKeyForm(ResetPasswordKeyForm):
      def __init__(self, *args, **kwargs):
        super(PasswordResetKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password6'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-1','placeholder':'Enter confirm password','id':'password7'})
        self.fields['password2'].label="Confirm Password"
        
        
class PasswordSetForm(SetPasswordForm):
      def __init__(self, *args, **kwargs):
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2','placeholder':'Enter new password','id':'password8'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter confirm password','id':'password9'})
        self.fields['password2'].label="Confirm Password"
