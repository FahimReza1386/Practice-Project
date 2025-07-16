from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.



class UserType(models.IntegerChoices):
    customer = 1,("Customer")
    admin = 2,("Admin")
    superuser = 3,("SuperUser")


class UserManager(BaseUserManager):


    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("The Phone_number must be set."))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
            

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)   
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.superuser.value)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("is_staff must have is True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("is_superuser must have is True"))

        return self.create_user(phone_number, password, **extra_fields)
        
class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True, blank=False)
    first_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD= "phone_number"
    REQUIRED_FIELDS =[]
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}-{self.phone_number}"
    
class Gender(models.IntegerChoices):
    male= 1,("male")
    female= 2,("female")
    other= 3,("other")

class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number=PhoneNumberField(unique=True)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.other.value)
    image= models.ImageField(upload_to="profile/", default="profile/user1.jpg")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk, phone_number=instance.phone_number)

