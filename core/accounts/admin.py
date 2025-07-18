from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, UserSubscriptionModel
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model=User
    list_display = ("first_name", "phone_number", "is_verified", "type")
    list_filter = ("type", "is_verified")
    search_fields = ("phone_number", "first_name")
    ordering = ("-created_date",)
    fieldsets = (
        ('Authenticaton', {
            "fields" : (
                "phone_number", "password", "first_name"
            ),
        }),
        ("Permission", {
            "fields" : (
                "is_verified", "is_active", "is_staff", "is_superuser"
            ),
        }),
        ("Group Permission", {
            "fields" : (
                "groups", "user_permissions", "type"
            ),
        }),
        ("important Date", {
            "fields" : (
                "last_login",    
            ),
        }),
        ("Subscription Info", {
            "fields" : (
                "subscription",     
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes" : ("wide",),
            "fields" : ("phone_number", "password1", "password2", "is_staff", "is_active", "is_verified", "type", "subscription", "subscription_exp")
        }),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ("user", "first_name", "last_name", "phone_number")
    searching_fields= ("user", "phone_number", "first_name", "last_name")

class CustomSubsCriptionAdmin(admin.ModelAdmin):
    model=UserSubscriptionModel
    list_display = ("user", "subs_type", "start_date", "end_date")


admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(UserSubscriptionModel, CustomSubsCriptionAdmin)
admin.site.register(User, CustomUserAdmin)