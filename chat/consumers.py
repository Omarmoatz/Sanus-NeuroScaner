from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("test websokets")
        await self.accept()
