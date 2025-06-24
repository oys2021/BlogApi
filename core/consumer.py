from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BlogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "data": event["message"]
        }))
