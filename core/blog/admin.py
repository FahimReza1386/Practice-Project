# Django Imports
from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _

# Locale Imports
from .models import BlogModel, BlogImageModel, BlogCategoryModel, WishListModel

@admin.register(BlogModel)
class BlogModelAdmin(TranslationAdmin):
    list_display=("pk", "title")
    list_filter=("status", "type")
    ordering=("-created_date",)
    search_fields=("title",)

    group_fieldsets = True

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }




@admin.register(WishListModel)
class WishListModelAdmin(admin.ModelAdmin):
    list_display=("pk", "blog__title")
    search_fields=("blog__title",)

@admin.register(BlogImageModel)
class BlogImageModelAdmin(admin.ModelAdmin):
    list_display=("pk", "file", "blog")
    search_fields=("blog",)

@admin.register(BlogCategoryModel)
class BlogCategoryAdmin(DraggableMPTTAdmin, TranslationAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    )
    list_display_links = (
        'indented_title',
    )
    group_fieldsets = True

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }