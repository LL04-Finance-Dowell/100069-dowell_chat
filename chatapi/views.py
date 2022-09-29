from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import random,string
import uuid
#from django.contrib.auth.models import User

from .models import Room, Message,User
from .serializers import RoomSerializer, MessageSerializer

from .connection import connection,get_event_id
from .population import targeted_population

#view to create a new room with a unique room link with admin

@csrf_exempt
@api_view(['POST'])
def create_room(request):
    user_name =  request.data['user_name']
    qrid = request.data['qrid']
    proj_lead = User.objects.filter(role='Proj_Lead').first()
    room_name = f"{user_name}_{qrid}"
    print(user_name,qrid,room_name,proj_lead)
    try: 
        user = User.objects.get(username=user_name)
    except:
        #create a new user
        user = User.objects.create_user(username=user_name,role='User')
    
    try:
        room = Room.objects.get(room_name=room_name)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except:
        #create room
        room = Room.objects.create(room_name=room_name)
        room.members.add(user, proj_lead)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


#add new member to the room
@csrf_exempt
@api_view(['POST'])
def add_member(request):
    user_name =  request.data['user_name']
    room = request.data['room']
    try: 
        user = User.objects.get(username=user_name)
    except:
        #create a new user
        user = User.objects.create_user(username=user_name,role='User')
    try:
        room = Room.objects.get(room_name=room)
        user = User.objects.get(username=user)
        room.add_members(user)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except:
        return Response({"Error":"User or Room does not exist"})

#send message to the room
@csrf_exempt
@api_view(['POST'])
def send_message(request):
    room =  request.data['room']
    sender =  request.data['sender']
    receiver = request.data['receiver']
    message = request.data['message']
    print(room,sender,receiver,message)
    sender = User.objects.get(username=sender)
    receiver = User.objects.get(username=receiver)
    room = Room.objects.get(room_name=room)
    #check if user is a member of the room
    if sender in room.members.all():
        message = Message.objects.create(room=room, sender=sender,receiver=receiver, message=message)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    else:
        return Response({"Error":"User is not a member of the room"})



#view to get all messages in a room
@csrf_exempt
@api_view(['GET','POST'])
def get_messages(request):
    room = request.data['room']
    try:
        room = Room.objects.get(room_name=room)
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response({"Error":"Room does not exist"})


#get room details
@csrf_exempt
@api_view(['GET','POST'])
def get_room(request):
    room = request.data['room']
    print(room)
    try:
        room = Room.objects.get(room_name=room)
        serializer = RoomSerializer(room)
        print(serializer.data)
        return Response(serializer.data)
    except:
        return Response({"Error":"Room does not exist"})


#get all rooms
@csrf_exempt
@api_view(['GET','POST'])
def get_rooms(request):
    all_rooms = Room.objects.all()
    user_name = request.data['user_name']
    role = request.data['role']
    try:
        user = User.objects.get(username=user_name)
        #check user role
        if user.role == 'Proj_Lead':
            if all_rooms:
                serializer = RoomSerializer(all_rooms, many=True)
                return Response(serializer.data)
            else:
                return Response({"Error":"No rooms exist"})
    except:
        #create a new user with role
        user = User.objects.create_user(username=user_name,role=role)
        serializer = RoomSerializer(all_rooms, many=True)
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
