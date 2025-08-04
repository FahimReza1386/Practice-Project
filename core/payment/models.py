# Django Imports
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# third party
from utils.models import AbstractBaseDateModel
from accounts.models import UserSubscriptionTypeModel

User= get_user_model()

class PaymentModel(AbstractBaseDateModel):
   
    class PaymentStatusModel(models.IntegerChoices):
        pending= 1, "در انتظار"
        success= 2, "پرداخت موفق"
        failed= 3, "پرداخت ناموفق"


    authority_id= models.CharField(
        max_length=300
    )
    user_subscriptiontype=models.IntegerField(
        choices=UserSubscriptionTypeModel.choices, 
        default=UserSubscriptionTypeModel.no_subscription.value,
        verbose_name=_("اشتراک")
    )
    amount= models.DecimalField(
        decimal_places=0, 
        max_digits=10, 
        default=0,
        verbose_name=_("مبلغ کل")
    )
    status= models.IntegerField(
        choices=PaymentStatusModel.choices, 
        default=PaymentStatusModel.pending.value,
        verbose_name=_("وضعیت")
    )
    ref_id=models.BigIntegerField(
        null=True, 
        blank=True
    )
    response_code= models.IntegerField(
        null=True, 
        blank=True
    )