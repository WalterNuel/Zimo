from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import *
from main.models import *
# Create your views here.

def lobby(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)

  suggest = Profile.objects.all()
  suggested = []
  btn_txt = 'View'

  for i in suggest:
    user_ = User.objects.get(username=i.username)
    if user_object == user_:
      pass
    else:
      try: 
        FollowerCount.objects.get(user=user_, follower = request.user.username)
        pass
      except:
        suggested.append(i)

  
  suggested = suggested[0:3]

  #User Search functionality
  search_input = request.GET.get('search-area')
  if search_input:
    small_case = search_input.lower()
    header = 'Showing results for'
    users = User.objects.all()
    suggested = []
    for i in users:
      if small_case in i.first_name.lower() or small_case in i.last_name.lower() or small_case in i.username.lower():
        profiles = Profile.objects.get(username = i)
        if FollowerCount.objects.filter(follower=request.user.username, user=i.username):
          btn_txt = 'Unfollow'
        else:
          btn_txt = 'Follow'
        suggested.append(profiles)
      else:
        pass
  else:
    header = 'Suggested Users'


  my_lobbies = Lobby.objects.filter(host=user_object)

  lobbies = Lobby.objects.all()

  context = {
    'user_object':user_object, 
    'user_profile':user_profile, 
    'header':header,
    'search':search_input,
    'suggest':suggested,
    'my_lobbies':my_lobbies,
    'all_lobbies':lobbies
    }


  return render(request, 'lobby.html', context)


def messages(request, uuid):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)

  active_lobby = Lobby.objects.get(id=uuid)

  all_members = Member.objects.filter(joined_lobby=active_lobby)
  len_of_members = len(all_members)
  lobby_members =[]

  for i in all_members:
    user_obj = User.objects.get(username=i.profile)
    profile_obj = Profile.objects.get(username=user_obj)

    lobby_members.append(profile_obj)
  
  date_in = []

  host_acc = User.objects.get(username=active_lobby.host)
  host_profile = Profile.objects.get(username=host_acc)
  
  msgs = LobbyMsgs.objects.filter(home=uuid)
  for i in msgs:
    user = User.objects.get(username=i.profile)
    profile = Profile.objects.get(username=user)
    i.profile_img = profile.profile_img
    i.name = str(user.username)
    i.save

    try:
      Member.objects.get(joined_lobby=i.home, profile=i.profile)
      pass
    except:
      member = Member.objects.create(joined_lobby=i.home, profile=i.profile)
      member.save()
    

  context = {
    "user_object":user_object,
    'user_profile':user_profile,
    'current_lobby':active_lobby,
    'messages':msgs,
    'len_of_members':len_of_members,
    'host':host_profile,
    'members':lobby_members,
    'test_join':all_members
  }

  return render(request, 'lobby-main.html', context)


def msg_upload(request, uuid):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)

  if request.method == 'POST':
    home = Lobby.objects.get(id=uuid)
    text_body = request.POST['text_body']
    profile = user_profile
    name = request.user.username
    profile_img = user_profile.profile_img

    if text_body == '':
      return redirect('lobby-message', uuid)

    new_msg = LobbyMsgs.objects.create(home=home, text_body=text_body, profile=profile, profile_img=profile_img, name=name)
    new_msg.save()
    return redirect('lobby-message', uuid)