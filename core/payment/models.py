# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Locale Imports
from utils.models import AbstractBaseDateModel
from subscriptions.models import Subscriptions

class PaymentModel(AbstractBaseDateModel):
   
    class PaymentStatusModel(models.IntegerChoices):
        pending= 1, "در انتظار"
        success= 2, "پرداخت موفق"
        failed= 3, "پرداخت ناموفق"


    authority_id= models.CharField(
        max_length=300
    )
    user_subscriptiontype=models.ForeignKey(
        Subscriptions,
        on_delete=models.PROTECT,
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

    class Meta:
        verbose_name= _("پرداخت")
        verbose_name_plural= _("پرداخت")