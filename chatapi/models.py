from django.db import models
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

#custom user model
class User(AbstractUser):
    choices = (
        ('Admin','Admin'),
        ('User','User'),
        ('Proj_Lead','Proj_Lead'),
    )
    role = models.CharField(max_length=10,choices=choices)

    def __str__(self):
        return self.username

class Room(models.Model):
    room_name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.room_name}"
    
    # def get_absolute_url(self):
    #     return reverse('room_detail', args=[str(self.id)])

    # # #populating the room with the proj_lead and user
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.members.add(self.proj_lead)
    #     self.members.add(self.user)
    
    #add new members to the room
    @property
    def add_members(self,*args):
        self.members.add(*args)

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    #receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.message
    class Meta:
        ordering = ['-timestamp']