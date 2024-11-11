from django.shortcuts import render, get_object_or_404
from .models import Room, Message
from django.contrib.auth.decorators import login_required

@login_required
def room_view(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    messages = room.messages.order_by('timestamp')
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})
