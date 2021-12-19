"""
Handling permissions for editors who are assigned to perform few important actions.
e.g. create article, moderate user profiles, department and other academic moderations.
UserTypes: Editor, AcademicOfficer
"""
from django.utils.translation import gettext_lazy as _

from .base import user_is_verified


def user_is_broker(user):
    """Permission to edit the academic session

    Args:
        user staff: a staff with an editor role

    Returns:
        true: if user is editor
    """
    return user_is_verified(user) and user.user_type == 2 \
        if user.is_authenticated else False

def user_is_investor(user):
    """Permission to approve, discipline and decline a student, teacher or guardian application

    Args:
        user staff: a staff with academic officer role
    """
    return user_is_verified(user) and user.user_type == 1 \
        if user.is_authenticated else False






# def user_is_non_academic(user):
#     """Non Academic Staff like cleaners, security

#     Args:
#         user staff: a staff user with a role as non acadmic who has no right with any academic affair or activity
#     Returns:
#         [type]: [description]
#     """
#     return user_is_verified(user) and user.teacher.staff_role == 1 \
#         if user.is_authenticated else False

# def user_is_lecturer(user):
#     """Permission granted to teacher/lecturers to be able to create videos, live streams and publish researched findings or [ublications for students

#     Args:
#         user staff: this is the lecturer or teacher in an academic structure
#     """
#     return user_is_verified(user) and user.teacher.staff_role == 2 \
#         if user.is_authenticated else False


# def user_is_editor_or_officer(user):
#     return user_is_editor(user) or user_is_academic_officer(user) \
#         if user.is_authenticated else False


# def user_is_vc(user):
#     return user_is_editor_or_officer(user) and user.teacher.staff_role == 5 \
#         if user.is_authenticated else False


# def user_is_dvc(user):
#     return user_is_editor_or_officer(user) and user.teacher.staff_role == 5 \
#         if user.is_authenticated else False

    
# def user_is_hod(user):
#     return user_is_lecturer(user) or user_is_academic_officer(user) \
#         if user.is_authenticated else False


# def user_is_dean(user):
#     return user_is_lecturer(user) or user_is_academic_officer(user) \
#         if user.is_authenticated else False
