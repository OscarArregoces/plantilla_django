from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)
from .view import AuthLoginFuncionario, LogoutView

app_name = "module"

urlpatterns = [
    path("login/", AuthLoginFuncionario.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
]
