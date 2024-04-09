from django.db import models
from django.conf import settings
# Create your models here.

User=settings.AUTH_USER_MODEL



class Room(models.Model):
    name=models.CharField(max_length=150,null=True,blank=True)
    first_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    second_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever')
    create_time=models.DateTimeField(auto_now_add=True)
    uid=models.CharField(max_length=150,null=True,blank=True)


    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content