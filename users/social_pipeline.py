import hashlib
from rest_framework.response import Response
# from rest_social_auth import strategy


def auto_logout(*args, **kwargs):
    """Do not compare current user with new one"""
    return {'user': None}


def save_avatar(response, user, **kwargs):
    pass


def check_for_email(backend, uid, user=None, *args, **kwargs):
    pass
