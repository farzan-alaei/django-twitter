import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message,Room
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model  # Import the user model class

User=get_user_model()
class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def create_chat(self, sender, msg):
        user=User.objects.get(email=sender)
        room=Room.objects.get(uid=self.scope["url_route"]["kwargs"]["room_name"])
        return Message.objects.create(room=room,sender=user, content=msg)
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json['user']
        
        if user != self.scope["user"]:  # Skip saving the message if the sender is the current user
            await self.create_chat(user, message)
                
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
                                   "message": message,
                                   "user": user
}
        )



    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["user"]
        email_sender= self.scope["user"]
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,'sender':sender
}))

