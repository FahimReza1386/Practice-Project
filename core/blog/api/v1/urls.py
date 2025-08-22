# django imports
from django.urls import path

# locale imports
from . import views

app_name="api-rest"

urlpatterns = [
    path("list/", views.ListBlogRestView.as_view(), name="api-blog-list"),
    path("detail/<int:pk>/", views.RetrieveBlogRestView.as_view(), name="api-blog-detail"),
]