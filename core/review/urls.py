from django.urls import path
from . import views

app_name="review"

urlpatterns =[
    path("create/", views.ReviewCreateView.as_view(), name="review-create"),
    path("delete/<int:pk>/", views.ReviewDeleteView.as_view(), name="review-delete"),
    path("reply/", views.ReviewReplyView.as_view(), name="review-reply"),
]   