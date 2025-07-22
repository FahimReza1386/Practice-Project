from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from shop.models import BlogCategoryModel
from accounts.models import User, UserSubscriptionTypeModel, UserSubscriptionModel
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.


class HomeView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = BlogCategoryModel.objects.all()
        return context
    
class ContactView(TemplateView):
    template_name = "website/contact.html"

class SubscriptionsView(TemplateView):
    template_name= "website/subscriptions.html"