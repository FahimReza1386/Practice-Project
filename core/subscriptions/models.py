# Django Imports 
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# ThirdParty Modules
from utils.models import AbstractBaseDateModel

class Subs_Buy(AbstractBaseDateModel):
    user =models.ForeignKey(
        "accounts.User", 
        on_delete=models.CASCADE,
        verbose_name=_("کاربر")
    )
    subscription=models.ForeignKey(
        "Subscriptions",
        on_delete=models.CASCADE,
        verbose_name=_("اشتراک")
    )
    start_date= models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("زمان شروع")
    )
    end_date= models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("زمان پایان")
    )
    is_active= models.BooleanField(
        default=False,
        verbose_name=_("فعال")
    )

    
    def is_valid(self):
        return self.is_active and self.end_date > timezone.now()
    
    def get_remaining_days(self):
        if self.is_valid():
            rammining_date= self.end_date - timezone.now()
            return rammining_date.days
        return timedelta(0)

    def __str__(self):
        return f"{self.user.first_name}-{self.is_active}"



class Subscriptions(AbstractBaseDateModel):
    class SubscriptionType(models.IntegerChoices):
        publish= 1, _("نمایش")
        draft= 2, _("عدم نمایش")

    name=models.CharField(
        max_length=200,
        verbose_name=_("نام اشتراک")
    )
    price= models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        default=0,
        verbose_name=_("مبلغ اشتراک")
    )
    discount_percent=models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("درصد تخفیف")
    )
    days=models.IntegerField(
        default=1,
        verbose_name=_("روز")
    )
    type=models.IntegerField(
        choices=SubscriptionType.choices,
        default=SubscriptionType.publish.value,
        verbose_name=_("وضعیت نمایش")
    )

    def __str__(self):
        return f"{self.name}-{self.price}"