from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Blog(models.Model):
    image = models.ImageField(upload_to='images/', default='images/Placeholder.png', blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("blog_list")
