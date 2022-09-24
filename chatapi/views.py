from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import random,string
import uuid
from django.contrib.auth.models import User

from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer

from .connection import connection,get_event_id
from .population import targeted_population

#view to create a new room with a unique room link with admin

@csrf_exempt
@api_view(['POST'])
def create_room(request):
    user_name =  request.data['user_name']
    session_id = request.data['sessionId']
    #admin_name = User.objects.get(username='admin')
    admin_name = User.objects.filter(is_superuser=True).first()
    room_name = f"{user_name}_{admin_name} Room"
    room_link = str(uuid.uuid4())[0:6]
    print(user_name,admin_name,room_name,room_link,session_id)
  
    try: 
        user = User.objects.get(username=user_name)
    except:
        #create a new user
        user = User.objects.create_user(username=user_name)
    
    try:
        room = Room.objects.get(sessionId=session_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except:
        #create room
        room = Room.objects.create(room_name=room_name,admin_name=admin_name,user_name=user,room_link=room_link,sessionId=session_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


#add new member to the room
@csrf_exempt
@api_view(['POST'])
def add_member(request):
    user_name =  request.data['user_name']
    room_link = request.data['room_link']
    try:
        room = Room.objects.get(room_link=room_link)
        user = User.objects.get(username=user_name)
        room.add_members(user)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except:
        return Response({"Error":"User or Room does not exist"})

#send message to the room
@csrf_exempt
@api_view(['POST'])
def send_message(request):
    user_name =  request.data['user_name']
    room_link = request.data['room_link']
    message = request.data['message']
    try:
        user = User.objects.get(username=user_name)
        room = Room.objects.get(room_link=room_link)
        #check if user is a member of the room
        if user in room.members.all():
            message = Message.objects.create(room=room, user=user, message=message)
            serializer = MessageSerializer(message)
            return Response({"Message Sent":serializer.data})
        else:
            return Response({"Error":"User is not a member of the room"})
    except:
        return Response({"Error":"User or Room does not exist"})


#view to get all messages in a room
@csrf_exempt
@api_view(['GET','POST'])
def get_messages(request):
    room_link = request.data['room_link']
    try:
        room = Room.objects.get(room_link=room_link)
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages":serializer.data,'room_link':room_link,'room_name':room.room_name})
    except:
        return Response({"Error":"Room does not exist"})


#get room details
@csrf_exempt
@api_view(['GET','POST'])
def get_room(request):
    room_link = request.data['room_link']
    try:
        room = Room.objects.get(room_link=room_link)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except:
        return Response({"Error":"Room does not exist"})


#get all rooms
@csrf_exempt
@api_view(['GET','POST'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

#get all data from the database and send to the dowell remote mongodb server
@csrf_exempt
@api_view(['GET','POST'])
def chat_end(request):
    room_link = request.data['room_link']
    room = Room.objects.get(room_link=room_link)
    messages = Message.objects.filter(room=room)
    # rooms = Room.objects.all()
    # messages = Message.objects.all()
    serializer = RoomSerializer(room)
    serializer1 = MessageSerializer(messages, many=True)

    data = {
        "rooms":serializer.data,
        "messages":serializer1.data
    }

    command = "insert"
    eventId = get_event_id()
    output = connection(command,eventId,data)

    return Response({"New Chat Created":output})


@csrf_exempt
@api_view(['GET'])
def get_chat_server(request):
    resp = targeted_population("hr_hiring","dowelltraining",["data"],"life_time")
    return Response(resp['normal']['data'][0])
