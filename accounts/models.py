from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# This is  a custom user model that inherits from the built-in AbstractUser model.
# It allows you to add custom fields or methods to the user model.
class CustomUser(AbstractUser):
    pass

# This is a model for storing customer photos. It has a date field that automatically sets the
# date and time when the photo is added, a photo field that stores the image, and a user field that
# is a foreign key to the CustomUser model.
class CustomerPhoto(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='users/', default='users/profile_placeholder.jpg', blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)