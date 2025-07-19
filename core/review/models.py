from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from shop.models import BlogModel

User = get_user_model()
# Create your models here.

class ReviewStatusModel(models.IntegerChoices):
    pending= 1, ("در انتظار تایید")
    accepted= 2, ("تایید شده")
    rejected= 3, ("لغو شده")


class ReviewModel(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    blog= models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    description=RichTextUploadingField(max_length=300)
    rate= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    status= models.IntegerField(choices=ReviewStatusModel.choices, default=ReviewStatusModel.pending.value)

    created_date= models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)

    def __str__(self):  
        return f"{self.user.first_name}-{self.blog.title}"