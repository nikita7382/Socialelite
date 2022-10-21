from distutils.command.upload import upload
from random import choices
from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True)
    bio=models.TextField(null=True,blank=True)
    avatar=models.ImageField(upload_to='displaypic',default='defaultpic.png')
    coverpic=models.ImageField(upload_to='coverpic',default='defaultcoverpic.jpg')

    # USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

class Post(models.Model):
    auther=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    postimage=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    posted_at=models.DateTimeField(auto_now_add=True)
    liked=models.ManyToManyField(User,default=None,related_name='liked',blank=True)

    class Meta:
        ordering=['-posted_at']

    def __str__(self):
        return str(self.id)

    @property
    def num_likes(self):
        return self.liked.all().count()

class Like(models.Model):
    
    viewer=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.post)

class Comment(models.Model):
    commented_at=models.DateTimeField(auto_now_add=True)
    commenter=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    body=models.TextField()
    
    class Meta:
        ordering=['-commented_at']

    def __str__(self):
        return str(self.body)

class follower_count(models.Model):
    viewing_user=models.CharField(max_length=200)

    profile_user=models.CharField(max_length=200)

    def __str__(self):
        return str(self.viewing_user)

    
