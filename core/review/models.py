# Django Imports

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Third Party
from utils.models import AbstractBaseDateModel
from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import BlogModel

User = get_user_model()

class ReviewModel(AbstractBaseDateModel):
    class ReviewStatusModel(models.IntegerChoices):
        pending= 1, ("در انتظار تایید")
        accepted= 2, ("تایید شده")
        rejected= 3, ("لغو شده")

    user= models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("کاربر")
    )
    blog= models.ForeignKey(
        BlogModel,
        on_delete=models.CASCADE,
        verbose_name=_("بلاگ")
    )
    description=RichTextUploadingField(
        max_length=300,
        verbose_name=_("جزئیات")
    )
    rate= models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=1,
        verbose_name=_("ستاره")
    )
    status= models.IntegerField(
        choices=ReviewStatusModel.choices, 
        default=ReviewStatusModel.pending.value,
        verbose_name=_("وضعیت")
    )

    def __str__(self):  
        return f"{self.user.first_name}-{self.blog.title}"