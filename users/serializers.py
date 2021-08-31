from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of User model
    """

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user.save()

        return user

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise ValidationError('Passwords doesnt match')
        validate_password(password=data.get('password'))

        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
