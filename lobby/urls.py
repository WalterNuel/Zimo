from django.urls import path
from . import views

urlpatterns = [
  path("", views.lobby, name="lobby"),
  path("<uuid>", views.messages, name="lobby-message"),
  path("upload/<uuid>", views.msg_upload, name="lobby-upload"),
]
