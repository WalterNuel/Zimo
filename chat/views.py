from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User, auth
from .models import *
from lobby.models import *
from main.models import *

# Create your views here.
def chat(request, pk):
  chatView ='n'
  rooms = ChatRoom.objects.all()

  for i in rooms:
    if i.userA == request.user.username and i.userB == pk:
      chatView = 'y'
      return redirect(f'/chat/main/{i.id}')
    elif i.userB == request.user.username and i.userA == pk:
      chatView = 'y'
      return redirect(f'/chat/main/{i.id}')
  
  if chatView != 'y':
    rooms = ChatRoom.objects.create(userA=request.user.username, userB=pk)
    rooms.save()
    return redirect(f'/chat/main/{rooms.id}')

  return HttpResponse(f'<h1>{request.user.username}:{pk}</h1>')        

#Chat Screen
def chat_screen(request, uuid):
  chat = ChatRoom.objects.get(id=uuid)
  chat_msg = ChatMsg.objects.filter(home=chat)

  current_user = request.user.username

  sending_user = ''
  sending_profile = ''

  receiving_user = ''
  receiving_profile = ''


  if chat.userA == current_user or chat.userB == current_user:
    if chat.userA == current_user:
      sending_user = User.objects.get(username=chat.userA)
      sending_profile = Profile.objects.get(username=sending_user)

      receiving_user = User.objects.get(username=chat.userB)
      receiving_profile = Profile.objects.get(username = receiving_user)

    elif chat.userB == current_user:
      sending_user = User.objects.get(username=chat.userB)
      sending_profile = Profile.objects.get(username=sending_user)

      receiving_user = User.objects.get(username=chat.userA)
      receiving_profile = Profile.objects.get(username = receiving_user)


    my_lobbies = Member.objects.filter(profile=sending_profile)
    common = []
    if my_lobbies:
      for i in my_lobbies:
        member_check = Member.objects.filter(profile=receiving_profile)
        if member_check:
          for k in member_check:
            if i.joined_lobby == k.joined_lobby:
              the_lobby = Lobby.objects.get(id=i.joined_lobby.id)
              common.append(the_lobby)
        else:
          pass
    else:
      pass

    len_for_common = len(common)

    

  context = {
    'chat':chat,
    'user':sending_profile,
    'receiver':receiving_profile,
    'msg':chat_msg,
    'lobbies':common,
    'no_of_lobbies':len_for_common,
  }

  return render(request, 'chat.html', context)
  

def msg_upload(request, uuid):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)

  if request.method == 'POST':
    home = ChatRoom.objects.get(id=uuid)
    text_body = request.POST['text_body']
    profile = user_profile
    name = request.user.username
    profile_img = user_profile.profile_img

    if text_body == '':
      return redirect(f'/chat/main/{uuid}')

    new_msg = ChatMsg.objects.create(home=home, text_body=text_body, profile=profile, name=name)
    new_msg.save()
    return redirect(f'/chat/main/{uuid}')