import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        partner = self.scope['url_route']['kwargs']['id']
        users = [user.username, partner]
        # users.sort()
        self.room_group_name = f'chat_{users[0]}__{users[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        async def receive(self, text_data):
            data = json.loads(text_data)
            messege = data['messege']
            await self.chanel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'messege': messege
                }
            )

        async def disconnect(self, close_code):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        async def chat_message(self, event):
            messege = event['messege']
            await self.send(text_data=json.dumps({'messege': messege}))
