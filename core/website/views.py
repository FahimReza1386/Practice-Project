# Django Imports

from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from datetime import timedelta


# Third Party
from blog.models import BlogCategoryModel
from accounts.models import User, UserSubscriptionTypeModel, UserSubscriptionModel


class HomeView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["genres"] = BlogCategoryModel.objects.all()
        return context

    
    
class ContactView(TemplateView):
    template_name = "website/contact.html"

class SubscriptionsView(TemplateView):
    template_name= "website/subscriptions.html"