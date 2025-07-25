from django.contrib import admin
from .models import PaymentModel
# Register your models here.
@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=("user_subscriptiontype", "status", "amount", "response_code", "authority_id")
    list_filter=("status", "response_code")
    searching_fileds=("user__title",)

