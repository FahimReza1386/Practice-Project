from django.contrib import admin
from .models import BlogModel, BlogImageModel, BlogCategoryModel, WishListModel
# Register your models here.

@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display=("pk", "title")
    list_filter=("status", "type")
    ordering=("-created_date",)
    search_fields=("title",)


@admin.register(BlogCategoryModel)
class BlogCategoryModelAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    search_fields=("name",)
    ordering=("-created_date",)

@admin.register(WishListModel)
class WishListModelAdmin(admin.ModelAdmin):
    list_display=("pk", "blog__title")
    search_fields=("blog__title",)

@admin.register(BlogImageModel)
class BlogImageModelAdmin(admin.ModelAdmin):
    list_display=("pk", "file", "blog")
    search_fields=("blog",)