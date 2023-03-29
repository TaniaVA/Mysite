from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

class CustomerPhoto(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField()
    photo = models.ImageField(upload_to='users/', default='users/profile-placeholder.png', blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
