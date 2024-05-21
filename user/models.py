from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    follower_count = models.IntegerField()
    following_count = models.IntegerField()
