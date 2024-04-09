from django.contrib import admin
from .models import User,UserFollowing
# Register your models here.



    
@admin.register(UserFollowing)
class UserFollowerAdmin(admin.ModelAdmin):
    list_display=['user_id','following_user_id']
    
class FollowerInline(admin.TabularInline):
    model = UserFollowing
    fk_name='user_id'

class FollowingInline(admin.TabularInline):
    model = UserFollowing
    fk_name='following_user_id'
   
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['email','mobile']
    inlines = [
        FollowerInline,FollowingInline
    ]
