import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Circle, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.circle_id = self.scope['url_route']['kwargs']['circle_id']
        self.room_group_name = f'circle_{self.circle_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        if not await self.user_is_member(user):
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message', '').strip()
        if not message_text:
            return

        user = self.scope['user']
        message = await self.save_message(user, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_name': user.name,
                'created_at': message.created_at.strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def user_is_member(self, user):
        return Circle.objects.filter(pk=self.circle_id, members=user).exists()

    @database_sync_to_async
    def save_message(self, user, text):
        circle = Circle.objects.get(pk=self.circle_id)
        return Message.objects.create(circle=circle, sender=user, text=text)