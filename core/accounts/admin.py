from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
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
                "phone_number", "password"
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
    )
    add_fieldsets = (
        (None, {
            "classes" : ("wide",),
            "fields" : ("phone_number", "password1", "password2", "is_staff", "is_active", "is_verified", "type")
        }),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ("user", "first_name", "last_name", "phone_number")
    searching_fields= ("user", "phone_number", "first_name", "last_name")


admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)