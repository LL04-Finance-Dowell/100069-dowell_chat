from rest_framework import serializers
from .models import Room, Message,User

class RoomSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ['room_name', 'members']

class MessageSerializer(serializers.ModelSerializer):
    room = serializers.ReadOnlyField(source='room.room_name')
    sender = serializers.ReadOnlyField(source='sender.username')
    # receiver = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['room','sender','message']