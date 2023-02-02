from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils.timezone import now

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profile_pictures", default="blank-profile-picture.png"
    )
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id_user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_pisctures")
    caption = models.TextField()
    created_at = models.DateTimeField(default=now())
    likes = models.IntegerField(default=0)
    username = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.username


class LikePost(models.Model):
    post_id = models.CharField(max_length=600)
    username = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.username


class FollowerCount(models.Model):
    follower = models.CharField(max_length=40)
    user = models.CharField(max_length=40)

    def __str__(self):
        return self.user
