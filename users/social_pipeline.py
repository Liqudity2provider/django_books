"""
This file makes work of social-auth-app-django correct and return a user: None when logging as new user
"""


def auto_logout(*args, **kwargs):
    """Do not compare current user with new one"""
    return {'user': None}
