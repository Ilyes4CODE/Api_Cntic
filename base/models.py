from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=190)
    picture = models.ImageField(null=True,default='Default_pfp.jpg')
    email = models.EmailField(max_length=190, null=True)
    phone = models.CharField(max_length=15, null=True)
    univ_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    content = models.CharField(max_length=500)
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE,blank=True)
    created_time = models.DateTimeField(auto_now_add=True,blank=True)
    likers = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikers = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

    def __str__(self):
        return self.content
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    comments = models.ManyToManyField(Comment, blank=True)
    likers = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    dislikers = models.ManyToManyField(User, related_name="disliked_posts", blank=True)
    like_count = models.IntegerField(null=True, blank=True,default=0)
    dislike_count = models.IntegerField(null=True, blank=True,default=0)
    

    def __str__(self):
        return self.content[:5]


class Event(models.Model):
    count = models.IntegerField()
    enrolled_users = models.ManyToManyField(User)


