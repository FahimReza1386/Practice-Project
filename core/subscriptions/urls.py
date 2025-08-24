# Django Imports
from django.urls import path, include

# Third Party Modules
from . import views


app_name="subscriptions"
urlpatterns=[
    path("list/", views.SubscriptionsListView.as_view(), name="subs-list"),
    path("api/v1/", include("subscriptions.api.v1.urls")),
]