from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,default=None,on_delete=models.CASCADE,related_name='author')
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)
    last_edited_at = models.DateTimeField(blank=True,null=True)
    

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,default=None,on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True, related_name='profile')
    bio = models.TextField()
    image=models.ImageField(upload_to='uploads/',blank=True,null=True,default='uploads/profileUserDefaultImg.png')
    blockedUsers = models.ManyToManyField(User, blank=True,related_name='blockedUsers')

    def __str__(self):
        return str(self.user)
