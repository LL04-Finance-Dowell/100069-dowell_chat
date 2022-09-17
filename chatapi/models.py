from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    admin_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    room_link = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name
    
    def get_absolute_url(self):
        return reverse('room_detail', args=[str(self.id)])

    #populating the room with the admin and user
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.members.add(User.objects.get(username=self.admin_name))
        self.members.add(User.objects.get(username=self.user_name))
    
    #add new members to the room
    def add_members(self, user):
        self.members.add(user)

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_at']