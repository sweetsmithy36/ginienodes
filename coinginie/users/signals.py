# from datetime import datetime

# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.core.mail import EmailMessage, send_mail, send_mass_mail
# from django.db.models import F
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.template.loader import render_to_string

# from coinginie.utils.rand_string import unique_number_generator
# from coinginie.wallet.models import Wallet

# from .models import AccountSettings, Investor, PrivacyPolicies

# User = get_user_model()

# today = datetime.today()




# # user signals

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         Investor.objects.create(user=instance)
#         AccountSettings.objects.create(user=instance)
#         PrivacyPolicies.objects.create(user=instance)
#         Wallet.objects.create(user=instance, bitcoin_balance=0.00, litecoin_balance=0.00, ethereum_balance=0.00 )
        
#         if instance.investor_id is None:
#             instance.investor_id = unique_number_generator(instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.investor.save()
#         instance.account.save()
#         instance.wallet.save()
#         instance.userprivacypolicy.save()

