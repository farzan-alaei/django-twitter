import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message,Room
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def create_chat(self, sender, msg):

        room=Room.objects.get(uid=self.scope["url_route"]["kwargs"]["room_name"])
        return Message.objects.create(room=room,sender=sender, content=msg)
    
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
        new_msg = await self.create_chat(email_sender, message)  # It is necessary to await creation of messages

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,'sender':sender
}))

