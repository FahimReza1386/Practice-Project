# Django Imports 
from django.urls import path

# Locale Imports
from . import views

app_name="api-rest"
urlpatterns =[
    path("jwt/login/", views.JWTLoginView.as_view(), name="jwt-login"),
    path("jwt/refresh/", views.JWTRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", views.JWTVerifyView.as_view(), name="jwt-verify"),
]