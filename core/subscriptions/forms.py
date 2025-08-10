# Django Imports

from django import forms

# Third Party Modules
from .models import Subscriptions


class SubscriptionsListForm(forms.ModelForm):
    class Meta:
        model=Subscriptions
        fields=["name", "price", "discount_percent", "days"]