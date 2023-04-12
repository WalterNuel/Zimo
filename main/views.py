from django.shortcuts import render, redirect
# from itertools import chain
# from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

@login_required(login_url='login')
def index(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)
  user = User.objects.all()
  posts = Post.objects.all()
  comments = Comment.objects.all()

  like_visual = "Likes"
  comment_visual = "Comments"
  save_visual = "Saves"

  for i in posts:
    liked = LikePost.objects.filter(post_id=i.id)
    commented = Comment.objects.filter(post_id=i.id)
    saved = SavePost.objects.filter(post_id=i.id)
    if len(liked) != i.no_of_likes:
      i.no_of_likes = len(liked)
      i.save()
      if len(liked) == 1:
        like_visual = "Like"
    else:
      pass
    if len(commented) != i.no_of_comments:
      i.no_of_comments = len(commented)
      i.save()
      if len(commented) == 1:
        comment_visual = "Comment"
    else:
      pass
    if len(saved) != i.no_of_saves:
      i.no_of_saves = len(saved)
      i.save()
      if len(saved) == 1:
        save_visual = "Sa"
    else:
      pass


  #Save or Unsave post checking
  saved_posts = SavePost.objects.filter(user=request.user.username)
  saved = []

  for i in saved_posts:
    save_filter = Post.objects.get(id=i.post_id)
    if save_filter:
      saved.append(save_filter)
    else:
      pass

  #Like or Liked post checking
  liked_posts = LikePost.objects.filter(user=request.user.username)
  liked = []

  for i in liked_posts:
    like_filter = Post.objects.get(id=i.post_id)
    if like_filter:
      liked.append(like_filter)
    else:
      pass
  

  following = []

  #Update post author account changes to post info
  for k in user:
    user_obj = User.objects.get(username=k)
    profile_obj = Profile.objects.get(username=user_obj)
    posts_obj = Post.objects.filter(author=user_obj)

    try: 
      FollowerCount.objects.get(user=k.username, follower=request.user.username)
      pass
    except:
      following.append(k)

    for i in posts_obj:
      author_profile = Profile.objects.get(username=i.author)
      if i.author_img != author_profile.profile_img:
        i.author_img = author_profile.profile_img
        i.save()

  #Suggested User display
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
        

  context = {
    'user_object':user_object, 
    'user_profile':user_profile,
    'display':posts,
    'suggest':suggested,
    'following':following,
    'header':header,
    'search':search_input,
    'btn_txt':btn_txt,
    'liked':liked,
    'saved':saved,
    'likes':like_visual,
    'comments':comment_visual,
    'saves':save_visual
    }

  return render(request, 'home.html', context)




@login_required(login_url='login')
def post_info(request, uuid):
  main_post = Post.objects.get(id=uuid)
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(username=user_object)
  comments = Comment.objects.filter(post_id=str(uuid))
  all_liked = LikePost.objects.all()

  for i in comments:
    profile_acc = Profile.objects.get(username=i.author)
    if i.author_img != profile_acc.profile_img:
      i.author_img = profile_acc.profile_img
      i.save
    else:
      pass

  comments_length = len(comments)

  #Like or Liked post checking
  saved_posts = SavePost.objects.filter(user=user_object)
  saved = []

  for i in saved_posts:
    save_filter = Post.objects.get(id=i.post_id)
    if save_filter:
      saved.append(save_filter)
    else:
      pass

  #Like or Liked post checking
  liked_posts = LikePost.objects.filter(user=user_object)
  liked = []

  for i in liked_posts:
    like_filter = Post.objects.get(id=i.post_id)
    if like_filter:
      liked.append(like_filter)
    else:
      pass

  #Suggested User display
  suggest = Profile.objects.all()
  suggest = suggest[0:5]
  btn_txt = 'View'


  #User Search functionality
  search_input = request.GET.get('search-area')
  if search_input:
    small_case = search_input.lower()
    header = 'Showing results for'
    users = User.objects.all()
    suggest = []
    for i in users:
      if small_case in i.first_name.lower() or small_case in i.last_name.lower() or small_case in i.username.lower():
        profiles = Profile.objects.get(username = i)
        if FollowerCount.objects.filter(follower=request.user.username, user=i.username):
          btn_txt = 'Unfollow'
        else:
          btn_txt = 'Follow'
        suggest.append(profiles)
      else:
        pass
  else:
    header = 'Suggested Users'

  context ={
    'user_object':user_object, 
    'user_profile':user_profile,
    'post':main_post,
    'suggest':suggest,
    'header':header,
    'search':search_input,
    'btn_txt':btn_txt,
    'liked':liked,
    'comments':comments,
    'amount':comments_length
  }

  return render(request, 'post.html', context)


@login_required(login_url='login')
def media(request, uuid):
  post = Post.objects.get(id=uuid)

  context = {
    'post':post,
  }

  return render(request, 'media.html', context)



@login_required(login_url='login')
def profile(request, pk):
  user_main = User.objects.get(username=request.user.username)
  profile_main = Profile.objects.get(username=user_main)

  user_object = User.objects.get(username=pk)
  user_profile = Profile.objects.get(username=user_object)
  user_posts = Post.objects.filter(author=user_object)

  for i in user_posts:
    if i.no_of_likes != 0:
      liked = LikePost.objects.filter(post_id=i.id)
      if len(liked) != i.no_of_likes:
        i.no_of_likes = len(liked)
        i.save()

  #Save or Unsave post checking
  saved_posts = SavePost.objects.filter(user=pk)
  saved = []

  for i in saved_posts:
    save_filter = Post.objects.get(id=i.post_id)
    if save_filter:
      saved.append(save_filter)
    else:
      pass

  #Like or Liked post checking
  liked_posts = LikePost.objects.filter(user=pk)
  liked = []

  for i in liked_posts:
    like_filter = Post.objects.get(id=i.post_id)
    if like_filter:
      liked.append(like_filter)
    else:
      pass

  following = FollowerCount.objects.filter(follower=pk)
  
  list_following = []

  for i in following:
    user_obj = User.objects.get(username=i.user)
    profile_obj = Profile.objects.get(username=user_obj)
    list_following.append(profile_obj)

  posts_figure = len(user_posts)

  follower = request.user.username
  user = user_object

  if FollowerCount.objects.filter(follower=follower, user=user):
    btn_txt = 'Unfollow'
  else:
    btn_txt = 'Follow'

  user_followers = len(FollowerCount.objects.filter(user=pk))
  user_following = len(FollowerCount.objects.filter(follower=pk))

  context = {
    'user_object':user_object, 
    'user_profile':user_profile, 
    'user_main':user_main, 
    'profile_main':profile_main, 
    'user_posts':user_posts, 
    'posts_figure':posts_figure,
    'btn_txt': btn_txt,
    'user_followers': user_followers,
    'user_following': user_following, 
    'list_following':list_following,
    'liked':liked,
    'saved':saved
  }

  return render(request, 'profile.html', context)


@login_required(login_url='login')
def like_post(request, uuid):
  liked_post = Post.objects.get(id=uuid)
  user_obj = request.user.username

  like_filter = LikePost.objects.filter(post_id=liked_post.id, user=user_obj)

  if like_filter:
    like_filter.delete()
    liked_post.no_of_likes = liked_post.no_of_likes - 1
    liked_post.save()
    return redirect('index')
    
  else:
    new_like = LikePost.objects.create(post_id=liked_post.id, user=user_obj)
    new_like.save()
    liked_post.no_of_likes = liked_post.no_of_likes + 1
    liked_post.save()
    return redirect('index')


@login_required(login_url='login')
def save_post(request, uuid):
  saved_post = Post.objects.get(id=uuid)
  user_obj = request.user.username

  save_filter = SavePost.objects.filter(post_id=saved_post.id, user=user_obj)

  if save_filter:
    save_filter.delete()
    saved_post.no_of_saves = saved_post.no_of_saves - 1
    saved_post.save()
    return redirect('index')
    
  else:
    new_save = SavePost.objects.create(post_id=saved_post.id, user=user_obj)
    new_save.save()
    saved_post.no_of_saves = saved_post.no_of_saves + 1
    saved_post.save()
    return redirect('index')



@login_required(login_url='login')
def follow(request, pk):
  user = pk
  follower = request.user.username


  if FollowerCount.objects.filter(follower=follower, user=user).first():
    delete_follower = FollowerCount.objects.get(follower=follower, user=user)
    delete_follower.delete()
    return redirect('/home/profile/'+user)
  else:
    new_follower = FollowerCount.objects.create(follower=follower, user=user)
    new_follower.save()
    return redirect('/home/profile/'+pk)

    # return redirect('index')




@login_required(login_url='login')
def upload(request):
  user_object = User.objects.get(username=request.user.username)
  author_profile = Profile.objects.get(username=user_object)


  # if request.method == 'POST':
  #   author_img = author_profile.profile_img
  #   author_first = author_profile.first_name
  #   author_last = author_profile.last_name
  #   author = User.objects.get(username=request.user.username)
  #   image = request.FILES.get('image_upload')
  #   text_written = request.POST['caption']
  #   caption = text_written.replace('\n', '<br>')
    
  #   if caption == "":
  #     return redirect('index', messages.info(request, "Entry can't be empty"))
    
  #   else:
  #     new_post = Post.objects.create(author=author, author_img=author_img, image=image, caption=caption, author_first=author_first, author_last=author_last)
  #     new_post.save()
  #     return redirect('index', messages.info(request, 'Uploaded'))
  # else:
  #   return redirect('index')

  context = {
    'user_profile':author_profile,
  }

  return render(request, 'upload-post.html', context)

  




@login_required(login_url='login')
def commenting(request, uuid):
  user_object = User.objects.get(username=request.user.username)
  author_profile = Profile.objects.get(username=user_object)
  if request.method == 'POST':
    author = user_object
    author_img = author_profile.profile_img
    comment_body = request.POST['comment']
    post_id = str(uuid)

    if comment_body == '':
      return redirect(f'/home/post/{str(uuid)}', messages.info(request, "Entry can't be empty"))
    else:
      new_comment = Comment.objects.create(author=author,author_img=author_img, comment_body=comment_body, post_id=post_id)
      post = Post.objects.get(id=uuid)
      post.no_of_comments += 1
      post.save()
      new_comment.save()
      return redirect(f'/home/post/{str(uuid)}', messages.info(request, 'Comment Uploaded'))



@login_required(login_url='login')
def settings(request, pk):
  user_object = User.objects.get(username=request.user)
  user_profile = Profile.objects.get(username=user_object)

  context =  {
    'user_objects':user_object,
    "user_profile": user_profile
  }

  if request.method == 'POST':
    if request.FILES.get('image') == None:
      image = user_profile.profile_img
      username = request.POST['username']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      bio = request.POST['bio']

      followers = FollowerCount.objects.filter(user=request.user.username)
      following = FollowerCount.objects.filter(follower=request.user.username)

      
      for i in followers:
        i.user = username
        i.save()
      for i in following:
        i.follower = username
        i.save()

      user_object.username = username
      user_object.first_name = first_name
      user_object.last_name = last_name
      user_object.save()

      
      user_profile.profile_img = image
      user_profile.username = User.objects.get(username=user_object.username)
      user_profile.first_name = first_name
      user_profile.last_name = last_name
      user_profile.bio = bio
      user_profile.save()
      return redirect('/home', messages.info(request, 'Profile Updated'))

    else:
      image = request.FILES.get('image')
      username = request.POST['username']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      bio = request.POST['bio']


      user_object.username = username
      user_object.first_name = first_name
      user_object.last_name = last_name
      user_object.save()
      
      user_profile.profile_img = image
      user_profile.username = User.objects.get(username=user_object.username)
      user_profile.first_name = first_name
      user_profile.last_name = last_name
      user_profile.bio = bio
      user_profile.save()
      return redirect('/home', messages.info(request, 'Profile Updated'))

  return render(request, 'settings.html', context)




def signup(request):
  if request.method == 'POST':
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username Taken')
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.save()

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(username=user_model, first_name=first_name, last_name=last_name)
        new_profile.save()
        return redirect('index')


  return render(request, 'signup.html')




def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('index')
    else:
      messages.info(request, "Invalid Input")
      return render(request, 'signin.html')

  return render(request, 'signin.html')



@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  return redirect('login')



# def lobby(request):
#   user_object = User.objects.get(username=request.user)
#   user_profile = Profile.objects.get(username=user_object)

#   suggest = Profile.objects.all()
#   my_lobbies = Lobby.objects.filter(host=user_object)

#   lobbies = Lobby.objects.all()

#   context = {
#     'user_object':user_object, 
#     'user_profile':user_profile, 
#     'suggest':suggest,
#     'my_lobbies':my_lobbies,
#     'all_lobbies':lobbies
#     }


#   return render(request, 'lobby.html', context)




def chat(request, pk):
  receiving_user = User.objects.get(username=pk)
  receiving_profile = Profile.objects.get(username=receiving_user)
  current_user = User.objects.get(username=request.user.username)
  current_profile = Profile.objects.get(username=current_user)

  # convo = Message.objects.get(sender=current_user, receiver=pk)

  suggest = Profile.objects.all()

  all_texts = []

  texts = Message.objects.filter(sender=current_user, receiver=pk)
  all_texts.append(texts)

  texts = Message.objects.filter(sender=pk, receiver=current_user)
  all_texts.append(texts)

  context = {
    'receiving_profile':receiving_profile,
    'current_user':current_user, 
    'current_profile':current_profile, 
    'suggest':suggest,
    'all_texts':all_texts
  }

  return render(request, 'chat.html', context)


# def messages_upload(request, pk):
#   receiving_user = User.objects.get(username=pk)
#   receiving_profile = Profile.objects.get(username=receiving_user)
#   current_user = User.objects.get(username=request.user.username)
#   current_profile = Profile.objects.get(username=current_user)

#   if request.method == 'POST':
#     sender = current_profile
#     receiver = receiving_profile
#     text_img = request.FILES.get('image_upload')
#     body_text = request.POST['caption']

#     new_post = Message.objects.create(sender=sender, receiver=receiver, text_img=text_img, body_text=body_text)
#     redirect('chat/<str:pk>')
#   else:
#     redirect('chat/<str:pk>')