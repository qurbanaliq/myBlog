from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """A model for a blog post"""
    title = models.CharField(max_length=300, blank=False)
    post_text = models.TextField(blank=False)
    date_published = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    views = models.IntegerField(default=0) # number of times the post viewed

    def __str__(self):
        return self.title

class Comment(models.Model):
    """A model for a comment on a blog post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, blank=False)
    time_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)