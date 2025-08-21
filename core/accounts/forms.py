# Django Imports

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Locale Imports

from accounts.models import User

class LoginForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(LoginForm, self).confirm_login_allowed(user) 
        if not user.is_verified:
            raise ValidationError(_("حساب کاربری فعال نیست .."))
    
class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["phone_number", "password"]