# Django Imports
from django.urls import path

# Third Party Modules
from . import views


app_name="subscriptions"
urlpatterns=[
    path("list/", views.SubscriptionsListView.as_view(), name="subs-list"),
]