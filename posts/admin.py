from django.contrib import admin
from posts.models import (
    Post, Comment, Reaction, Tag, Image, PostTagFollow
)


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'content', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content', 'created_at', 'updated_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image', 'is_featured', 'alt', 'created_at', 'updated_at']
