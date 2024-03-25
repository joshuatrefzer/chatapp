from rest_framework import serializers
from .models import Channel, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'created_at', 'source' , 'in_thread']
        
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'description', 'members', 'is_channel', 'picture', 'read_by']
