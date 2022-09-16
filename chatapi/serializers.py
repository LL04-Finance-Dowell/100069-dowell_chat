from rest_framework import serializers
from .models import Room, Message

class RoomSerializer(serializers.ModelSerializer):
    admin_name = serializers.ReadOnlyField(source='admin_name.username')
    user_name = serializers.ReadOnlyField(source='user_name.username')
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ['room_name', 'admin_name', 'user_name', 'room_link', 'members']

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    room = serializers.ReadOnlyField(source='room.room_name')
    class Meta:
        model = Message
        fields = ['room', 'user', 'message']