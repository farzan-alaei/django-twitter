from django.contrib import admin
from .models import Message,Room
# Register your models here.

   
@admin.register(Room)
class roomAdmin(admin.ModelAdmin):
    list_display=['first_user','second_user','create_time','name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=['room','sender','content']
    