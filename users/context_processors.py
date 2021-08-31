from django.conf import settings

from users.utils import user_from_token


def social_app_keys(request):
    """Hand over values into template"""
    return {
        'facebook_key': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        'googleoauth2_key': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
    }


def hand_over_user(request):
    """Hand over user value into template"""

    context_data = dict()

    if request.COOKIES:
        context_data['jwt_user'] = user_from_token(request.COOKIES.get('token'))

    return context_data
