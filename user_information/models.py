from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models




## task2
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no phone_number field."""

    def _create_user(self, username,phone_number, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
     #    email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, username,phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone_number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username,phone_number, password, **extra_fields)

        


class CustomUser(AbstractUser):
     gender_list = [('female','female'), ('male', 'male')]
     # username = None
     phone_number = PhoneNumberField(unique=True)
     country_code = CountryField(blank=True, null=True)
     gender = models.CharField(max_length=30, choices=gender_list,blank=True, null=True)
     birthdate = models.DateField(blank=True, null=True)
     avatar = models.ImageField(upload_to="images/", blank=True, null=True)


     USERNAME_FIELD = 'phone_number'
     REQUIRED_FIELDS = ['username']

     objects: CustomUserManager()

     def __str__(self):
          return self.phone_number 







class Status(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    def __str__(self):
          return self.user.first_name 



