from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(FollowerCount)
admin.site.register(LikePost)
admin.site.register(Comment)
admin.site.register(LikeComment)