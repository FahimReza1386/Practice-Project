from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from .forms import LoginForm, RegisterForm
import random
# Create your views here.

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    
class LogOutView(auth_views.LogoutView):
    pass

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "accounts/register.html"
    model=User
    form_class= RegisterForm
    success_url= reverse_lazy("accounts:login")
    success_message= "حساب کاربری شما با موفقیت ساخته شد .."

    def create_otp(self):
        random_letter = chr(random.choice([random.randint(97, 122), random.randint(65, 90)]))
        random_number = random.randint(0, 1000000)
        otp_code = f"{random_number}{random_letter}"
        return otp_code

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["otp_code"] = self.create_otp()
        return context