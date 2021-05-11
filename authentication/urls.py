from django.urls import path
from .views import register_user, login_user, user_detail, logout_user

urlpatterns = [
    path('users/register',register_user),
    path('users/login',login_user),
    path('users/logout',logout_user),
    path('users/',user_detail)
]