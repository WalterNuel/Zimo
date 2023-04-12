from django.db import models
from main.models import Profile, User, Post

import random, uuid, string
from datetime import datetime
from django.utils import timezone

# Create your models here.
class ChatRoom(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  userA = models.CharField(max_length=100)
  userB = models.CharField(max_length=100)
  active_date = models.DateTimeField(auto_now_add=True)


class ChatMsg(models.Model):
  home = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  text_body = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=30, default='user', null=False)
  time_sent = models.DateTimeField(auto_now_add=True)

  def time(self):
    check = self.time_sent.day
    ago = timezone.now() - self.time_sent

    if self.time_sent.hour > 12:
        hours = '{:02d}:{:02d} pm'.format(self.time_sent.hour, self.time_sent.minute)
    else:
        hours = '{:02d}:{:02d} am'.format(self.time_sent.hour, self.time_sent.minute)

    return hours
