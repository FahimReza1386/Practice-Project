# Django Imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from decimal import Decimal 
from django.utils.translation import gettext_lazy as _

# Locale Imports
from utils.models import AbstractBaseDateModel

# Third Party 

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

class BlogModel(AbstractBaseDateModel):

    class BlogStatusTypeModel(models.IntegerChoices):
        publish= 1, _("نمایش")
        draft= 2, _("عدم نمایش")
    
    class BlogTypeModel(models.IntegerChoices):
        premium= 1, _("ویژه")
        normal= 2, _("عادی")

    title= models.CharField(
        max_length=200,
        verbose_name=_("اسم")
    )
    description=RichTextUploadingField(
        verbose_name=_("توضیحات"),
    )
    type= models.IntegerField(
        choices=BlogTypeModel.choices,
        default=BlogTypeModel.normal.value,
        verbose_name=_("نوع")
    )
    status= models.IntegerField(
        choices=BlogStatusTypeModel.choices, 
        default=BlogStatusTypeModel.publish.value,
        verbose_name=_("وضعیت")
    )
    price= models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name=_("مبلغ")
    )
    discount_percent= models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("درصد تخفیف")
    )
    image= models.ImageField(
        upload_to="blogs/", 
        default="blogs/image.jpg",
        verbose_name=_("تصویر")
    )
    category= models.ForeignKey(
        "BlogCategoryModel",
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("دسته بندی")
    )


    class Meta:
        verbose_name=_("پست ها")
        verbose_name_plural=_("پست ها")

    def __str__(self):
        return f"{self.title}{self.pk}"
    
    def is_discounted(self):
        return self.discount_percent != 0
    
    def get_price_after_sale(self):
        amout_price = self.price * Decimal(self.discount_percent/100)
        price= self.price - amout_price
        return round(price)

class BlogImageModel(AbstractBaseDateModel):
    blog = models.ForeignKey(
        BlogModel, 
        on_delete=models.CASCADE,
        verbose_name=_("بلاگ")
    )
    file= models.ImageField(
        upload_to="blogs/extra_img/",
        verbose_name=_("تصویر")
    )



    class Meta:
        verbose_name=_("عکس پست ها")
        verbose_name_plural = _("عکس پست ها")


    def __str__(self):
        return f"{self.blog.title}"
    

class BlogCategoryModel(MPTTModel):
    name= models.CharField(
        max_length=100,
    )
    parent= TreeForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="children"
    )

    class MPTTMeta:
        order_insertion_by= ["name"]

    class Meta:
        verbose_name=_("دسته بندی ها")
        verbose_name_plural=_("دسته بندی ها")

    def __str__(self):
        return f"{self.pk}-{self.name}"
    

class WishListModel(AbstractBaseDateModel):
    blog=models.ForeignKey(
        BlogModel, 
        on_delete=models.CASCADE,
        verbose_name=_("بلاگ")
    )
    user=models.ForeignKey(
        "accounts.User", 
        on_delete=models.CASCADE,
        verbose_name= _("کاربر")
    )

    class Meta:
        unique_together = ('user', 'blog')
        verbose_name = _("علاقه مندی ها")
        verbose_name_plural = _("علاقه مندی ها")

    def __str__(self):
        return f"{self.blog.title}-{self.pk}"