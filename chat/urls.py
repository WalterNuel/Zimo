from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [
  path("<pk>", views.chat, name="chat-main"),
  path("main/<uuid>", views.chat_screen, name="chat-screen"),
  path("chat-upload/<uuid>", views.msg_upload, name="chat-upload"),
]