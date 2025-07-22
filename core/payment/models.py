from django.db import models
from accounts.models import UserSubscriptionTypeModel
from django.contrib.auth import get_user_model

User= get_user_model()
# Create your models here.

class PaymentStatusModel(models.IntegerChoices):
    pending= 1, "در انتظار"
    success= 2, "پرداخت موفق"
    failed= 3, "پرداخت ناموفق"

class PaymentModel(models.Model):
    authority_id= models.CharField(max_length=300)
    user_subscriptiontype=models.IntegerField(choices=UserSubscriptionTypeModel.choices, default=UserSubscriptionTypeModel.no_subscription.value)
    amount= models.DecimalField(decimal_places=0, max_digits=10, default=0)
    status= models.IntegerField(choices=PaymentStatusModel.choices, default=PaymentStatusModel.pending.value)
    ref_id=models.BigIntegerField(null=True, blank=True)
    response_code= models.IntegerField(null=True, blank=True)
    created_date= models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)