from django.contrib import admin
from .models import ReviewModel, ReviewStatusModel
# Register your models here.

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("user__first_name", "blog__title", "pk", "status")
    list_filter= ("status",)
    search_fields= ("user__first_name", "blog__title")