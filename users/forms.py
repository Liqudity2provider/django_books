from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """
    Form for creating User model
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating User model
    """

    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email']


class UserLoginForm(forms.ModelForm):
    """
    Form for login User model
    """

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'password']

