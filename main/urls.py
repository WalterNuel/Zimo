from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("follow/<str:pk>", views.follow, name="follow"),

    path("save-post/<uuid>", views.save_post, name="save-post"),
    path("like-post/<uuid>", views.like_post, name="like-post"),
    path("post/<uuid>", views.post_info, name="post-main"),
    path("post/media/<uuid>", views.media, name="post-media"),
    path("post-comment/<uuid>", views.commenting, name="comment-upload"),
    path("upload", views.upload, name="upload"),
    path("settings/<str:pk>", views.settings, name="settings"),

    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]
