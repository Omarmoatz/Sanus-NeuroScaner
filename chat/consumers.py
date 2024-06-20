import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            chat_with_user = self.scope['url_route']['kwargs']['username']
            users = [user.username, chat_with_user]
            users.sort()
            self.room_group_name = f'chat_{users[0]}__{users[1]}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

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

        
