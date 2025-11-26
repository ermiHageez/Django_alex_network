import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async  
from .models import Mentor, ChatMessage

logger = logging.getLogger(__name__)

class MentorChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.mentor_id = self.scope['url_route']['kwargs']['mentor_id']
        except Exception:
            logger.exception("Failed to get mentor from scope url_route")
            await self.close(code=4001)
            return

        self.room_group_name = f'mentor_{self.mentor_id}'
        logger.info("WebSocket connect attempt: startup_id=%s, channel=%s", self.mentor_id, self.channel_name)

        # Join room group
        try:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            logger.info("WebSocket accepted: %s", self.room_group_name)
        except Exception:
            logger.exception("Error accepting WebSocket or adding to group")
            await self.close(code=1011)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            logger.info("WebSocket disconnected: %s (code=%s)", self.room_group_name, close_code)
        except Exception:
            logger.exception("Error during WebSocket disconnect")

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            user = self.scope.get('user')

            logger.info("Received message from user=%s in startup=%s: %s", getattr(user, 'username', None), self.startup_id, message)

            # Save to database
            await self.save_message(getattr(user, 'id', None), self.startup_id, message)

            # Send message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': getattr(user, 'username', 'Anonymous'),
                }
            )
        except Exception:
            logger.exception("Error handling received message")