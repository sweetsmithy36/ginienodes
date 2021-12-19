"""Basic Settings for permissions and Roles.

Permissions for basic levell actions in the project.

Usertypes: Student, Teacher, Guardian
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


@login_required
def permission_error(request):
    return HttpResponse(_("You don't have the right permission to access this page"))

def user_is_verified(user):
    return user.is_verified == True if user.is_authenticated else False

def user_is_investor(user):
    return user_is_verified(user) and user.user_type == 1 \
        if user.is_authenticated else False

def user_is_broker(user):
    return user_is_verified(user) and user.user_type == 2 \
        if user.is_authenticated else False

