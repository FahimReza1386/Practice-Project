from django.urls import path
from . import views

app_name="review"

urlpatterns =[
    path("review/create/", views.ReviewCreateView.as_view(), name="review-create"),
    path("review/delete/<int:pk>/", views.ReviewDeleteView.as_view(), name="review-delete"),
]   