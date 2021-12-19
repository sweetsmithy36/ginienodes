from allauth.account.views import PasswordChangeView, PasswordSetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView

from coinginie.wallet.models import Transactions


# Create your views here.
class DashboardView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "Dashboard" 
        greeting['pageview'] = "Dashboards"
        greeting['transactions'] = Transactions.objects.filter(user=request.user).order_by("-created")[:10]
        greeting['deposits'] = Transactions.objects.filter(user=request.user, type="Invest").order_by("-created")[:10]
        greeting['withdrawals'] = Transactions.objects.filter(user=request.user, type="Withdraw").order_by("-created")[:10]
        return render (request,'dashboard/dashboard-crypto.html',greeting)

class DashboardTradeView(LoginRequiredMixin,View):
    def get(self,request):
        greeting = {}
        greeting['heading'] = "MT5 Trade View" 
        greeting['pageview'] = "MT5 Trade View"
        return render (request,'dashboard/dashboard-trade.html',greeting)

class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard')
    
class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('dashboard')
