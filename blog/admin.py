from django.contrib import admin
from .models import BlogPost, UserProfile, Comment

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(BlogPost)
admin.site.register(Comment)