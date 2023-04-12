from django.db import models
from main.models import Profile, User

import random, uuid, string
from datetime import datetime
from django.utils import timezone

# Create your models here.
def generate_unique_code():
  length = 6

  while True:
    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if Lobby.objects.filter(code=code).count() == 0:
      break

  return code


class Lobby(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  name = models.CharField(max_length=30, default="New Room", null=False)
  code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
  host = models.ForeignKey(User, on_delete=models.CASCADE)
  about = models.TextField(max_length=200, null=True)
  img = models.ImageField(upload_to='profile_images', default='lobby-img.png')
  created_at = models.DateTimeField(auto_now_add=True)
  no_of_members = models.IntegerField(default=0)

  def day(self):
    main = f'{self.created_at.date()}'
    return main



class LobbyMsgs(models.Model):
  home = models.ForeignKey(Lobby, on_delete=models.CASCADE)
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  text_body = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  name = models.CharField(max_length=30, default='user', null=False)
  profile_img = models.ImageField(upload_to='text_profiles', default='lobby-img.png')
  time_sent = models.DateTimeField(auto_now_add=True)

  def time(self):
    check = self.time_sent
    ago = timezone.now() - self.time_sent

    min = str(self.time_sent.minute)
    min = len(min)


    if self.time_sent.hour > 12:
      if min == 2:
        hours = f'{self.time_sent.hour}:{self.time_sent.minute} pm'
      else:
        hours = f'{self.time_sent.hour}:0{self.time_sent.minute} pm'
    else:
      if min == 2:
        hours = f'{self.time_sent.hour}:{self.time_sent.minute} am'
      else:
        hours = f'{self.time_sent.hour}:0{self.time_sent.minute} am'

    return hours


class Member(models.Model):
  joined_lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
  date_joined = models.DateTimeField(auto_now_add=True, null=True)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return self.profile.username.username

  def time(self):
    hour = self.date_joined
    return hour