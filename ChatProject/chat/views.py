import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Message, Room

logger = logging.getLogger(__name__)

def room_view(request, room_name):
    logger.debug(f"Accessing room: {room_name}")
    room, created = Room.objects.get_or_create(name=room_name)
    logger.info(f"Room: {room}, Created: {created}")
    messages = room.messages.order_by('timestamp')
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})
