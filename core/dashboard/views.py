from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile, UserSubscriptionModel, UserSubscriptionTypeModel
from jalali_date import datetime2jalali
from .forms import ProfileEditForm


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name="dashboard/home.html"    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_subscription= UserSubscriptionModel.objects.filter(user=self.request.user).exists()
            if user_subscription is True:
                subscription = UserSubscriptionModel.objects.get(user=self.request.user)
                context["ramming_days"] = subscription.get_remaining_days()
            else:
                context["ramming_days"] = "بدون اشتراک"
            jalali_join = datetime2jalali(self.request.user.created_date).strftime('%y/%m/%d')
            context["joined"]=jalali_join
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