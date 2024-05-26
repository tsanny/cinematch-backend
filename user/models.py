from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)


class UserFollowing(models.Model):
    user_id = models.ForeignKey("CustomUser",
                                related_name="following",
                                on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("CustomUser",
                                          related_name="followers",
                                          on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user_id", "following_user_id"]]
