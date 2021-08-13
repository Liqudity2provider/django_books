"""django_books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from users.views import LoginView
from users import views as user_views

urlpatterns = [
    path('', include('books.urls')),
    path('user/', include('users.urls')),

    path('login/', user_views.LoginView.as_view(), name='login'),
    path('register/', user_views.UserRegister.as_view(), name='register'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),

    path(r'^api/user/jwt/', user_views.UserJWTDetailView.as_view(), name="current_user_jwt"),

    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', include('rest_social_auth.urls_jwt_pair')),

]
