from django.contrib.auth.models import User
from rest_framework import generics
from users.serializers import UserSerializer


class UserApiListView(generics.ListCreateAPIView):
    """
        List all users, or create a new.
        """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User


class UserApiDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
