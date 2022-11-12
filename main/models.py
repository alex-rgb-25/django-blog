from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name="blog")
    title = models.CharField(max_length = 60)
    text = models.CharField(max_length=20000)
    url = models.CharField(max_length = 600, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    tags = TaggableManager()
    likes = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
    related_name="user_comment")
    text = models.CharField(max_length=1000)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
    related_name="blog_comments")
    
    def __str__(self):
        return self.text

class Likers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    related_name="liker") 
    #link info from one model to another  USER < -- > liked_blogs
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
    related_name="liked_blog")
