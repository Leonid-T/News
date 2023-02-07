from django.db import models

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    image = models.ImageField(default='default.jpg')
    tags = TaggableManager()
