from rest_framework import serializers
from .models import Channel, Message, Thread

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'created_at', 'source' ]
        
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'author', 'content', 'created_at', 'source' ]
        


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'description', 'members', 'is_channel', 'picture', 'read_by']