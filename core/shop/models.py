from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator 
# Create your models here.


class BlogTypeModel(models.IntegerChoices):
    permium= 1,("Permium")
    normal= 2,("Normal")


class BlogStatusTypeModel(models.IntegerChoices):
    publish= 1,("نمایش")
    draft= 2,("عدم نمایش")

class BlogModel(models.Model):
    title= models.CharField(max_length=200)
    description=RichTextUploadingField()
    type= models.IntegerField(choices=BlogTypeModel.choices, default=BlogTypeModel.normal.value)
    status= models.IntegerField(choices=BlogStatusTypeModel.choices, default=BlogStatusTypeModel.publish.value)
    image= models.ImageField(upload_to="blogs/")
    price= models.DecimalField(default=0, decimal_places=0, max_digits=10)
    discount_percent= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title-self.pk}"

class BlogImageModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    file= models.ImageField(upload_to="blogs/extra_img/")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.blog.title}"