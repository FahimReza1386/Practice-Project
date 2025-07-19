from django.urls import path
from . import views

app_name="dashboard"
urlpatterns = [
    path("home/", views.DashboardHomeView.as_view(), name="home"),
    path("security/edit/", views.DashboardSecurityEdit.as_view(), name="security-edit"),
    path("profile/edit/", views.DashboardProfileEdit.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.DashboardProfileImageEdit.as_view(), name="profile-image-edit"),
]