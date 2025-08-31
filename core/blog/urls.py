from django.urls import path, include
from . import views

app_name = "blog"
urlpatterns = [
    path("grid/", views.BlogGridView.as_view(), name="blog-grid"),
    path("detail/<int:pk>/", views.BlogDetailView.as_view(), name="blog-detail"),
    path("wishlist/add/", views.AddWishListView.as_view(), name="add-wishlist"),
    path("category/<int:pk>/", views.CategoriesView.as_view(), name="blog-category"),
    path("wishlist/blog/", views.WishListBlogPageView.as_view(), name="blog-wishlist"),
    path("api/v1/", include("blog.api.v1.urls")),
]