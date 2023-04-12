from django.db import models
import string
import random
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Profile(models.Model):
  username = models.ForeignKey(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  bio = models.TextField(blank=True)
  profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

  def __str__(self):
    return self.username.username


class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  author_img = models.ImageField(upload_to='post_author_images', blank=True)
  author_first = models.CharField(max_length=100, blank=True)
  author_last = models.CharField(max_length=100, blank=True)
  image = models.ImageField(upload_to='post_images', blank=True)
  caption = models.TextField()
  pub_date = models.DateTimeField(default=datetime.now)
  no_of_likes = models.IntegerField(default=0)
  no_of_comments = models.IntegerField(default=0)
  no_of_saves = models.IntegerField(default=0)

  def __uuid__(self):
    return self.id

  def time_posted(self):
    check = self.pub_date
    ago = timezone.now() - self.pub_date

    min = str(self.pub_date.minute)
    min = len(min)


    if self.pub_date.hour > 12:
      if min == 2:
        hours = f'{self.pub_date.hour}:{self.pub_date.minute} PM • {check.day}/{check.month}/{check.year}'
      else:
        hours = f'{self.pub_date.hour}:0{self.pub_date.minute} PM • {check.day}/{check.month}/{check.year}'
    else:
      if min == 2:
        hours = f'{self.pub_date.hour}:{self.pub_date.minute} AM • {check.day}/{check.month}/{check.year}'
      else:
        hours = f'{self.pub_date.hour}:0{self.pub_date.minute} AM • {check.day}/{check.month}/{check.year}'

    if ago.days == 1:
      hours = 'Yesterday'

    elif ago.days != 1 and ago.days < 1:
      if ago.seconds < 60:
        hours = f'Just Now'
      elif ago.seconds < (60 * 60):
        hours = f'Moments Ago'
      elif ago.seconds > (60 * 60):
        hours = f'Today'

    return hours


class LikePost(models.Model):
  post_id = models.CharField(max_length=500, default='')
  user = models.CharField(max_length=100, default='')

  def __str__(self):
    return self.post_id


class Comment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  post_id = models.CharField(max_length=500)
  comment_body = models.CharField(max_length=100, null=False)
  author_img = models.ImageField(upload_to='post_author_images', blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  pub_date = models.DateTimeField(default=datetime.now)
  no_of_likes = models.IntegerField(default=0)

  def __str__(self):
    return self.post_id

  def time(self):
    hours = timezone.now() - self.pub_date
    

    if hours.days > 7:
      hours = hours.days // 7
      hours = f'{hours}w'

    elif hours.days == 7:
      hours = 1
      hours = f'{hours}w'

    elif hours.days < 0 or hours.days == 0:
      hours = hours.seconds // 60
      if hours == 60 or hours > 60:
        hours = hours // 60
        hours = f'{hours}h'
      else:
        hours = f'{hours}m'
        
    else:
      hours = f'{hours.days}d'
       
    return hours

class LikeComment(models.Model):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Comments(models.Model):
#   post = models.ForeignKey(Post, on_delete=models.CASCADE)
#   user = models.ForeignKey(Profile, on_delete=models.CASCADE)

class SavePost(models.Model):
  post_id = models.CharField(max_length=500)
  user = models.CharField(max_length=500)

  def __str__(self):
    return self.post_id


class Message(models.Model):
  sender = models.CharField(max_length=100, default='')
  receiver = models.CharField(max_length=100, default='')
  body_text = models.TextField()
  text_img = models.ImageField(upload_to='text_images', blank=True)
  time_sent = models.DateTimeField(default=datetime.now)

  def __str__(self):
      return self.body_text
  

class FollowerCount(models.Model):
  follower = models.CharField(max_length=100)
  user = models.CharField(max_length=100)


  def __str__(self):
    return self.user