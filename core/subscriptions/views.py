# Django Imports
from django.shortcuts import render
from django.views.generic import ListView

# Third Party Modules
from .models import Subscriptions
from .forms import SubscriptionsListForm
from blog.filters import SubscriptionsFilter

class SubscriptionsListView(ListView):
    template_name="subscriptions/subs-list.html"
    model=Subscriptions
    form_class= SubscriptionsListForm

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["filter"] = SubscriptionsFilter(self.request.GET, queryset=Subscriptions.objects.filter(type=Subscriptions.SubscriptionType.publish.value))
        return context