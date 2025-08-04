# Django Imports
from django.contrib import admin

# Third Paty
from .models import ReviewModel

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("user__first_name", "blog__title", "pk", "status")
    list_filter= ("status", "rate")
    search_fields= ("user__first_name", "blog__title")