from django.urls import path

from coinginie.users.views import (
    PrivacyPolicyUpdate,
    SubscribePlans,
    UserBankUpdate,
    UserDocUpdate,
    UserUpdateView,
    close_account,
    kyc_verification,
    subscribe,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~subscription/contract/<int:pk>/", view=subscribe, name="subscribe"),
    path("~close/<str:username>/", view=close_account, name="close_account"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~contracts/", view=SubscribePlans.as_view(), name="plans"),
    path("~bank/", view=UserBankUpdate.as_view(), name="account"),
    path("~privacy/", view=PrivacyPolicyUpdate.as_view(), name="privacy"),
    path("~doc/", view=UserDocUpdate.as_view(), name="doc"),
    path("~update/", view=UserUpdateView.as_view(), name="profile"),
    path("~kyc/", view=kyc_verification, name="kyc"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
