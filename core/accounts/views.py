from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import LoginForm
# Create your views here.

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    