# Django Imports
from django.contrib import admin

# Third Party Modules
from .models import Subs_Buy, Subscriptions

@admin.register(Subs_Buy)
class Subs_BuyModelAdmin(admin.ModelAdmin):
    list_display=("user", "subscription", "start_date", "end_date", "is_active")
    list_filter= ("is_active", "subscription__name")
    ordering= ("-created_date",)

@admin.register(Subscriptions)
class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display=("name", "price", "discount_percent", "days", "type")
    list_filter= ("days", "name", "type")
    ordering= ("-created_date",)