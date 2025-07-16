from django.contrib import admin
from .models import BlogModel
# Register your models here.

@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display=("pk", "title")
    list_filter=("status", "type")
    ordering=("-created_date",)
    search_fields=("title",)
