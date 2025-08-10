# Django Imports
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _

# Third Party
from .models import BlogModel, BlogImageModel, BlogCategoryModel, WishListModel

@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display=("pk", "title")
    list_filter=("status", "type")
    ordering=("-created_date",)
    search_fields=("title",)

@admin.register(WishListModel)
class WishListModelAdmin(admin.ModelAdmin):
    list_display=("pk", "blog__title")
    search_fields=("blog__title",)

@admin.register(BlogImageModel)
class BlogImageModelAdmin(admin.ModelAdmin):
    list_display=("pk", "file", "blog")
    search_fields=("blog",)

admin.site.register(
    BlogCategoryModel,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)