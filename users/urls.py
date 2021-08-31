from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .api import UserApiListView, UserApiDetailView
from .utils import setcookie, getcookie

urlpatterns = [
    path("", UserApiListView.as_view(), name="all-users"),
    path("<int:pk>/", UserApiDetailView.as_view(), name="user"),
    path('scookie/', setcookie),
    path('gcookie/', getcookie)

]
urlpatterns = format_suffix_patterns(urlpatterns)
