from django.urls import path
from . import views


app_name = "website"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("subscriptions/", views.SubscriptionsView.as_view(), name="subscriptions"),
    path("AcceptedRequestBuy/<int:pk>/", views.AcceptedRequestBuy.as_view(), name="AcceptedRequestBuy"),
]