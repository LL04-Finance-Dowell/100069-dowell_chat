from django.contrib import admin
from .models import Room, Message,User
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name','created_at')
    list_filter = ('room_name','created_at')
    search_fields = ('room_name','created_at' )

admin.site.register(Room,RoomAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('room','sender','message','timestamp')
    list_filter = ('room','sender','message','timestamp')
    search_fields = ('room','sender','message','timestamp')

admin.site.register(Message,MessageAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role' ,'is_staff','product')
    list_filter = ('username', 'role' ,'is_staff','product')
    search_fields = ('username', 'role' ,'is_staff','product')

admin.site.register(User, UserAdmin)