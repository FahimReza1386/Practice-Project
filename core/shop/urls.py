from django.urls import path 
from . import views

app_name = "shop"
urlpatterns = [
    path("blog/grid/", views.BlogGridView.as_view(), name="blog-grid"),
    path("blog/detail/<int:pk>/", views.BlogDetailView.as_view(), name="blog-detail"),
    path("blog/wishlist/add/", views.AddWishListView.as_view(), name="add-wishlist"),
]