from django.urls import path, include

from . import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
    path('add-member/', views.add_member, name='add_member'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('get-room/', views.get_room, name='get_room'),
    path('get-rooms/', views.get_rooms, name='get_rooms'),
]
