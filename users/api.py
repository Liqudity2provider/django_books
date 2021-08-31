from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from users.serializers import UserSerializer


class UserApiListView(generics.ListCreateAPIView):
    """
    List all users, or create a new.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def __init__(self, *args, **kwargs):
        """Define number of objects per page"""

        self.pagination_class.default_limit = 10
        super().__init__(*args, **kwargs)


class UserApiDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
