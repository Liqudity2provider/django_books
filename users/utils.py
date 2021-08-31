import time
import jwt
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.backends import TokenBackend
from django_books import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse


def user_from_token(token):
    """
    Return User model from token by decoded id in token
    """

    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        user = User.objects.get(pk=user_id)
        return user
    except:
        return None


def get_tokens_for_user(user):
    """
    Retrieve User model and creates 'refresh' and 'token'
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }


def setcookie(request):
    """
    Set cookie
    """
    refresh = request.data['refresh']
    token = request.data['token']

    response = HttpResponse("Cookie Set")
    response.set_cookie('refresh', refresh)
    response.set_cookie('token', token)

    return response


def getcookie(request):
    """
    Return HTTP response with cookie
    """
    return HttpResponse(
        str(request.COOKIES)
    )


def check_expiration(token, refresh):
    """
    Retrieve 'token' and 'refresh', decodes it and check if time is expired.
    Refresh 'token' and return 'refresh' and 'token'
                                        OR return "token has been expired"
    """
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    if decoded_token.get('exp') > time.time():
        # if token not expired
        return None
    decoded_refresh = jwt.decode(refresh, options={"verify_signature": False})
    if decoded_refresh.get('exp') > time.time():
        refresh = RefreshToken(token=refresh)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
    return {
        'error': "token has been expired"
    }


def set_expiration_time_token(token, time_in_timestamp: int) -> 'changed encoded token':
    """
    Retrieve 'token' and time in timestamp, decode 'token', change date, encode and return
    """
    decoded = jwt.decode(token, options={"verify_signature": False})
    decoded['exp'] = time_in_timestamp
    return str(jwt.encode(decoded, key=settings.SECRET_KEY))


def refresh_token_or_redirect(request):
    """
    Get token from COOKIE
    Checking expiration using method 'check_expiration'
    """

    token = request.COOKIES.get('token')
    refresh = request.COOKIES.get('refresh')
    try:
        validation_result = check_expiration(token, refresh)

        if not validation_result:
            # if token not expired
            return token
        elif 'token' in validation_result.keys():
            # if token refreshed
            return str(token)
        else:
            messages.error(request, 'Your token has been expired. Please login again.')
            return {
                'error': 'token has been expired'
            }
    except:
        messages.error(request, 'Your token has been expired. Please login again.')
        return {
            'error': 'token has been expired'
        }
