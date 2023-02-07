from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    image = models.ImageField(default='default.jpg')
    tags = TaggableManager()
    views_count = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    def views_counter(self):
        self.views_count += 1
        self.save()

    def like_count(self):
        return self.like.all().count()

    def is_like(self, user):
        return self.like.filter(id=user.id).exists()

    def set_like(self, user):
        if self.is_like(user):
            self.like.remove(user)
            result = False
        else:
            self.like.add(user)
            result = True
        self.save()
        return result
