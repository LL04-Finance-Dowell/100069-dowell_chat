from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import random,string
import uuid
from django.contrib.auth.models import User
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
#view to create a new room with a unique room link with admin

@csrf_exempt
@api_view(['POST'])
def create_room(request):
    user_name =  request.data['user_name']
    admin_name = User.objects.get(username='admin')
    room_name = f"{user_name}_{admin_name}_{uuid.uuid4().hex[:6].upper()}"
    room_link = str(uuid.uuid4())
    #check if user exists
    if User.objects.filter(username=user_name).exists():
        room = Room.objects.create(room_name=room_name, admin_name=admin_name, user_name=user_name, room_link=room_link)

        serializer = RoomSerializer(room)

        return Response({"New Room Created":serializer.data})
    else:
        return Response({"Error":"User does not exist"})



#add new member to the room
@csrf_exempt
@api_view(['POST'])
def add_member(request):
    user_name =  request.data['user_name']
    room_link = request.data['room_link']
    room = Room.objects.get(room_link=room_link)
    user = User.objects.get(username=user_name)
    if user.exists():
        room.add_members(user)
        serializer = RoomSerializer(room)
        return Response({"New Member Added":serializer.data})
    else:
        return Response({"Error":"User does not exist"})

#send message to the room
@csrf_exempt
@api_view(['POST'])
def send_message(request):
    user_name =  request.data['user_name']
    room_link = request.data['room_link']
    message = request.data['message']
    room = Room.objects.get(room_link=room_link)
    user = User.objects.get(username=user_name)
    #check if user is a member of the room
    if user in room.members.all():
        message = Message.objects.create(room=room, user=user, message=message)
        serializer = MessageSerializer(message)
        return Response({"Message Sent":serializer.data})
    else:
        return Response({"Error":"You are not a member of this room"})


#view to get all messages in a room
@csrf_exempt
@api_view(['GET'])
def get_messages(request):
    room_link = request.data['room_link']
    room = Room.objects.get(room_link=room_link)
    messages = Message.objects.filter(room=room)

    serializer = MessageSerializer(messages, many=True)

    return Response({"Messages":serializer.data})


#get room details
@csrf_exempt
@api_view(['GET'])
def get_room(request):
    room_link = request.data['room_link']
    room = Room.objects.get(room_link=room_link)
    if room.exists():
        serializer = RoomSerializer(room)
        return Response({"Room Details":serializer.data})
    else:
        return Response({"Error":"Room does not exist"})


#get all rooms
@csrf_exempt
@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()

    serializer = RoomSerializer(rooms, many=True)

    return Response({"Rooms":serializer.data})
