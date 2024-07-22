from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomeUser(AbstractUser):
    email=models.EmailField(max_length=100,unique=True)
    isVerify=models.BooleanField(default=False)
    REQUIRED_FIELDS=["isVerify","email"]

class Comment(models.Model):
    author=models.ForeignKey(CustomeUser,related_name="like_user",on_delete=models.CASCADE)
    text=models.TextField(max_length=100)
    created_date=models.DateField(auto_now_add=True)

class Like(models.Model):
    author=models.ForeignKey(CustomeUser,related_name="comment_user",on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

class Post(models.Model):
    author=models.ForeignKey(CustomeUser,related_name="post_user",on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField(max_length=100)
    published_date=models.DateField(auto_now_add=True)
    comment=models.ManyToManyField(Comment,related_name='comment_posts', blank=True)
    like=models.ManyToManyField(Like,related_name='liked_posts', blank=True)

