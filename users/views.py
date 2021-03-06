import json
import requests
from django.shortcuts import redirect
from django.views.generic.detail import BaseDetailView
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login
from rest_social_auth.views import SimpleJWTAuthMixin
from django_books import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm
from django.contrib import messages
from .serializers import UserSerializer
from .utils import user_from_token, get_tokens_for_user, refresh_token_or_redirect

PATH = settings.URL_PATH

headers = {
    'Content-Type': 'application/json',
}


class UserRegister(generics.CreateAPIView):
    """
    User Register View returning:
    - GET request - return HTML page with Form (Register Form)
    - POST request - retrieve User data, creates new User and return Login page
    """

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            template_name='users/register.html', data={
                "form": UserRegisterForm,
            }
        )

    def post(self, request, *args, **kwargs):
        form_data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password1"),
            "password2": request.data.get("password2")
        }
        response = requests.post(
            PATH + 'api/users/',
            headers=headers,
            data=json.dumps(form_data)
        )

        output = response.json()
        if output.get("errors"):
            return Response(
                template_name='users/register.html', data={
                    "form": UserRegisterForm(),
                    "messages": [*output.get('errors')]
                }
            )

        return Response(
            template_name='users/login.html', data={
                "form": UserRegisterForm(),
            }
        )


class LoginView(APIView):
    """
    User Login View returning:
    - GET request - return HTML page with User Login Form
    - POST request - retrieve data, authenticate User, create 'token' and 'refresh' and set them as cookie

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        return Response(
            template_name='users/login.html', data={
                "form": UserLoginForm
            }
        )

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if not user:
            messages.error(request, "Cannot find user with this email and password")
            return Response(
                template_name='users/login.html', data={
                    "form": UserLoginForm
                }
            )

        else:
            pair_tokens = get_tokens_for_user(user)  # creating tokens for user authentication
            requests.get(
                PATH + 'books/api/',
                headers=self.headers,
                data=request.data,
            )
            response = redirect('books_main')
            response.set_cookie('refresh', pair_tokens["refresh"])
            response.set_cookie('token', pair_tokens["token"])
            return response


class LogoutView(APIView):
    """
    User Logout View returning:
    - GET request - delete cookie and return Logout HTML page   

    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(
            template_name='users/logout.html',
            data={
                'user': None
            }
        )
        response.delete_cookie('refresh')
        response.delete_cookie('token')

        return response


class UserJWTDetailView(SimpleJWTAuthMixin, BaseDetailView):
    """Used to send requests from js in templates"""
    pass
