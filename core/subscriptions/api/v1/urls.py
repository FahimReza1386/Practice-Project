# Django Imports
from django.urls import path

# Locale Imports
from . import views

app_name="api-rest"
urlpatterns=[
    path("list/", views.ApiListSubscriptionView.as_view(), name="api-subs-list"),
    path("create/", views.ApiCreateSubscriptionView.as_view(), name="api-subs-create"),
    path("detail/<int:pk>/", views.ApiDetailSubscriptionView.as_view(), name="api-subs-detail"),
    path("delete/<int:pk>/", views.ApiDeleteSubscriptionView.as_view(), name="api-subs-delete"),
]