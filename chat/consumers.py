import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        partner = self.scope['url_route']['kwargs']['id']
        users = [user.username, partner]
        # users.sort()  # Ensure consistent room names
        self.room_group_name = f'chat_{users[0]}__{users[1]}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('in connect after channel_layer ----------------------')
        await self.accept()
        

    async def receive(self, text_data):
        print(f'Received text_data: "{text_data}"')  # Log received data

        if not text_data:
            print('Empty message received')
            return

        try:
            data = json.loads(text_data)
            print(f'Parsed JSON data: {data}')

            message = data.get('message', '')
            if not message:
                print('No message content found in parsed data')
                return

            print('in receive-----------------------' + message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError as e:
            print(f'JSON decode error: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')


    async def disconnect(self, close_code):
        print('in disconnect----------------')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        print('in chat_message' + message)
        await self.send(text_data=json.dumps({'message': message}))
