from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("api/v1/", include("accounts.api.v1.urls")),
]