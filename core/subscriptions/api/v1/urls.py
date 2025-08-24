# Django Imports
from django.urls import path

# Locale Imports
from . import views

app_name="api-rest"
urlpatterns=[
    path("list/", views.ApiListSubscriptionView.as_view(), name="api-subs-list"),
    path("detail/<int:pk>/", views.ApiDetailSubscriptionView.as_view(), name="api-subs-detail"),
]