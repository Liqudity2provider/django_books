from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .api import UserApiListView, UserApiDetailView
from .utils import setcookie, getcookie
# from .views import UserList, UserDetail

urlpatterns = [
    # path("", UserList.as_view(), name="all-users"),
    path("", UserApiListView.as_view(), name="all-users"),
    path("<int:pk>/", UserApiDetailView.as_view(), name="user"),

    # path('<int:pk>/', UserDetail.as_view()),
    path('scookie/', setcookie),
    path('gcookie/', getcookie)

]
urlpatterns = format_suffix_patterns(urlpatterns)
