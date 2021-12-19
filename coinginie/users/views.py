from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from formtools.preview import FormPreview

from coinginie.contracts.models import Contract, Plans, Subscription
from coinginie.users.forms import (
    AccountSettingsForm,
    DocFileForm,
    InvestorForm,
    PrivacyPoliciesForm,
)
from coinginie.users.models import AccountSettings, Investor, PrivacyPolicies
from coinginie.wallet.models import Deposit, Transactions
from coinginie.wallet.tasks import send_admin_mail, send_deposit_mail

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['bankform'] = self.third_form_class(self.request.POST or None, instance=self.request.user.account)
        # context['imageform'] = self.fourth_form_class(self.request.POST or None, self.request.FILES, instance=self.request.user.userprofile)
        context['transactions'] = Transactions.objects.filter(user=self.request.user) 
        context['heading'] = "Profile" 
        context['pageview'] = "Profile"
        return context

user_detail_view = UserDetailView.as_view()

class UserBankUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AccountSettings
    form_class = AccountSettingsForm
    success_message = "Bank Information successfully updated"

    def get_success_url(self):
        return reverse("users:profile")

    def get_object(self):
        return self.request.user.account

class UserDocUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Investor
    form_class = DocFileForm
    success_message = "Documents successfully updated"

    def get_success_url(self):
        return reverse("users:profile")

    def get_object(self):
        return self.request.user.investor

# def  file_upload(request):
#     if request.method == "POST":
#         doc = request.FILES.get('file')
#         Investor.objects.filter(user=request.user).update(doc=doc)
#         return HttpResponse('')
#     return JsonResponse({'post':'false'})
    
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Investor
    template_name = "users/profile.html"
    form_class = InvestorForm
    # third_form_class = AccountSettingsForm
    # fourth_form_class = DocFileForm
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user.investor
    
    def form_valid(self, form):
        form.save()
        User.object.filter(username=self.request.user.username).update(profile_updated=True)   
        return super().form_valid(form)
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['bankform'] = self.third_form_class(self.request.POST or None, instance=self.request.user.account)
        # context['docform'] = self.fourth_form_class(self.request.POST or None, self.request.FILES, instance=self.get_object())
        context['heading'] = "Update Profile" 
        context['pageview'] = "Update Profile"
        return context


user_update_view = UserUpdateView.as_view()

@login_required
def kyc_verification(request):
    if request.method == 'POST':
        bankform = AccountSettingsForm(request.POST or None, instance=request.user.account)
        docform = DocFileForm(request.POST or None, request.FILES, instance=request.user.investor)

        if bankform.is_valid() and docform.is_valid():
            bankform.save()
            docform.save()
            
            to_email = request.user.email
            subject = "[GinieNodes] User Verification"
            body = f"""
            Dear {request.user.first_name},
            
            Your request to be verified is being processed.
            
            Please be patient
            
            Yours Truly
            Ginie Nodes
            """
            send_deposit_mail.delay(to_email, subject, body)

# ---------------------------------------------------------------------------

            admin_subject = "[User Verification Request] Admin Notice"
            admin_body = f"""
            {request.user.username} has requested to be verified.
            
            Confirm the information provided.
            
            Then verify them if they meet requirements.
            """
            admins = settings.ADMINS

            send_admin_mail.delay(admins, admin_subject, admin_body)

            # User.objects.filter(username=request.user.username).update(is_verified=True)
            return redirect(request.user.get_absolute_url())
    else:
        bankform = AccountSettingsForm()
        docform = DocFileForm()   
        
            
    return render(request, 'users/kyc.html', {'bankform':bankform,"docform":docform, "heading":"KYC Verification", "pageview":"KYC Verification"})
        
class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class PrivacyPolicyUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PrivacyPolicies
    template_name = "users/privacy.html"
    form_class = PrivacyPoliciesForm
    success_message = _("Privacy Settings successfully updated")
    
    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user.userprivacypolicy
    
    # def form_valid(self, form):
    #     form.save()
    #     return self.get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = "Privacy Settings" 
        context['pageview'] = "Privacy Settings"
        return context


def subscribe(request, pk):
    contract = get_object_or_404(Plans, pk=pk)
    if request.user.subscription:
        Subscription.objects.filter(user=request.user).update(contract=contract)
        return redirect(request.user.get_absolute_url())


class SubscribePlans(LoginRequiredMixin, ListView):
    model = Plans
    template_name = "users/plans.html"
    context_object_name = "objects"
    queryset = Plans.objects.all().order_by('created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = "Contracts" 
        context['pageview'] = "Contracts"
        return context
    
    
@login_required
def close_account(request, username):
    if not request.user:
        return reverse_lazy("home")
    
    user = get_object_or_404(User, username=username)
    User.objects.filter(username=user.username, is_active=True).update(is_active=False)
    messages.info(request, "Successfully Closed Account")
    return reverse_lazy('home')
