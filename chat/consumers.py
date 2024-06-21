import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        print(f"Connecting user: {user}")
        if not user.is_authenticated:
            print('User is not authenticated')
            await self.close()
            return
        
        partner_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{user.id}_{partner_id}'  # Temporary initialization

        partner = await self.get_user(partner_id)
        if not partner:
            print(f'Partner with ID {partner_id} does not exist')
            await self.close()
            return

        users = [user.username, partner.username]
        users.sort()  # Ensure consistent room names
        self.room_group_name = f'chat_{users[0]}__{users[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('in connect after channel_layer ----------------------')
        await self.accept()

    async def receive(self, text_data):
        if not text_data:
            print('Empty message received')
            return

        try:
            data = json.loads(text_data)
            message = data.get('message', '')
            if not message:
                print('No message content found in parsed data')
                return

            sender = self.scope['user']
            sender_user = await self.get_user(sender.id)
            if sender_user is None:
                print(f'Sender user with ID {sender.id} does not exist')
                return

            partner_id = self.scope['url_route']['kwargs']['id']
            receiver = await self.get_user(partner_id)
            if receiver is None:
                print(f'Receiver with ID {partner_id} does not exist')
                return

            # Save the message to the database
            await self.create_chat_message(sender_user, receiver, message)

            print('in receive------------' + message)
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
        print('disconnected--------------')
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def chat_message(self, event):
        message = event['message']
        print('in chat_message' + message)
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            print(f'Fetching user with ID {user_id}')
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            print(f'User with ID {user_id} does not exist')
            return None

    @database_sync_to_async
    def create_chat_message(self, sender, receiver, message):
        print(f'Creating message from {sender} to {receiver} with content: {message}')
        return ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
