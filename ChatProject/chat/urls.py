# ChatProject/chat/urls.py

from django.urls import path
from . import consumers
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.room_view, name='room'),
]