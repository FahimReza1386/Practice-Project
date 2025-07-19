from django.urls import path
from . import views

app_name="dashboard"
urlpatterns = [
    path("home/", views.DashboardHomeView.as_view(), name="home"),
]