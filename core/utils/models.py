# Django Imports

from django.db import models
from django.utils.translation import gettext_lazy as _

class AbstractBaseDateModel(models.Model):
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("زمان ایجاد شده")
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_("زمان بروزرسانی")
    )


    class Meta:
        abstract = True