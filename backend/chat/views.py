from django.shortcuts import render
from rest_framework import viewsets, status

from users.models import CustomUser
from .models import Channel, Message, Thread
from .serializers import ChannelSerializer, MessageSerializer, ThreadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
    
class ThreadViewset(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    

#austesten (Müsste nun geordnet sein nach Zeit) #auch thread Nachrichten sollen zurückkommen?? 
class Messages_and_Thread_from_Channel(APIView):
    def get(self, request, channel_id, format=None):
        messages = Message.objects.filter(source=channel_id).order_by('-created_at')
        message_serializer = MessageSerializer(messages, many=True)
        
        thread_messages = []
        
        for message in messages:
            thread = Thread.objects.filter(source=message.id)
            thread_messages.extend(thread)
        
        thread_serializer = ThreadSerializer(thread_messages, many=True)
        
        data = {
            'messages': message_serializer.data,
            'thread_messages': thread_serializer.data
        }
        return Response(data)
    


class Channel_and_Preview(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        channels = Channel.objects.filter(members=user)
        last_messages_from_channels = []

        for channel in channels:
            last_message = Message.objects.filter(source=channel.id).order_by('-created_at').first()
            if last_message:
                last_messages_from_channels.append(last_message)

        channel_serializer = ChannelSerializer(channels, many=True)
        message_serializer = MessageSerializer(last_messages_from_channels, many=True)
        
        data = {
            'channels': channel_serializer.data, 
            'preview-messages': message_serializer.data  
        }
        return Response(data)
    
    
    
class ThreadsFromMessages(APIView):
    def get(self, request, message_id, format=None):
        threads = Thread.objects.filter(source=message_id)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)
    
    
class ChannelsForUser(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        channels = Channel.objects.filter(members=user)
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)
    