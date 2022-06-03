from django.db import models
from django.contrib.auth.models import User
from yk.models import Profile

# Create your models here.
class Game(models.Model):
    content = models.TextField(verbose_name='Game_content', blank=True, null=True)
    def __str__(self):
        return self.content