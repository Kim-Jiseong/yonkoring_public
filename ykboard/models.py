from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager
from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey
from django.db import models
from datetime import datetime


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-create_at', 'author')

class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    order = models.TextField(null=True, default=None)
    reply = models.ForeignKey(
        'Comment', related_name='comments', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('create_at', 'post','author')

class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE, blank=True, null=True)