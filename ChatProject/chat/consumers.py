# chat/consumers.py
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, Room

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug(f"Connecting to chat")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting from chat")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        data = json.loads(text_data)
        message = data["message"]
        username = self.scope["user"].username

        # Save message to the database
        await self.save_message(username, self.room_name, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        logger.info(f"Sending message: {event}")
        # Called when a message is received in the room group
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

    @sync_to_async
    def save_message(self, username, room_name, message):
        logger.info(f"Saving message: {message}")
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        Message.objects.create(user=user, room=room, content=message)
