# Django Imports

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin

# Locale Imports

from accounts.models import Profile
from subscriptions.models import Subs_Buy, Subscriptions
from .forms import ProfileEditForm

# Third Party

from jalali_date import datetime2jalali



class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name="dashboard/home.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            # Get active subscription if exists
            active_subscription = Subs_Buy.objects.filter(
                user=user,
                is_active=True
            ).first()
            
            if active_subscription:
                context["remaining_days"] = active_subscription.get_remaining_days()
            else:
                context["remaining_days"] = "بدون اشتراک"
            
            # Convert join date to Jalali
            jalali_join = datetime2jalali(user.created_date).strftime('%y/%m/%d')
            context["joined"] = jalali_join
        
        return context


class DashboardSecurityEdit(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name="dashboard/security/security-edit.html"
    success_url= reverse_lazy("dashboard:home")
    success_message= "مشتری گرامی رمزعبور شما با موفقیت تغییر کرد ."

class DashboardProfileEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model=Profile
    form_class=ProfileEditForm
    success_message="مشتری گرامی اطلاعات پروفایل شما با موفقیت بروزرسانی شد .."
    success_url = reverse_lazy("dashboard:profile-edit")
    template_name="dashboard/security/profile-edit.html"

    def get_object(self, queryset = None):
        queryset =Profile.objects.get(user=self.request.user)
        return queryset

class DashboardProfileImageEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model=Profile
    success_message="مشتری گرامی عکس پروفایل شما با موفقیت بروزرسانی شد .."
    success_url = reverse_lazy("dashboard:profile-edit")
    http_method_names="post"
    fields = ("image",)
    def get_object(self, queryset = None):
        queryset =Profile.objects.get(user=self.request.user)
        return queryset