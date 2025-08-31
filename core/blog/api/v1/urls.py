# django imports
from django.urls import path

# locale imports
from . import views

app_name="api-rest"

urlpatterns = [
    path("list/", views.ListBlogRestView.as_view(), name="api-blog-list"),
    path("create/", views.CreateBlogRestView.as_view(), name="api-blog-create"),
    path("detail/<int:pk>/", views.DetailBlogRestView.as_view(), name="api-blog-detail"),
    path("delete/<int:pk>/", views.DeleteBlogRestView.as_view(), name="api-blog-delete"),
]