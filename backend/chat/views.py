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
    
    
class MessagesFromChannel(APIView):
    def get(self, request, channel_id, format=None):
        messages = Message.objects.filter(source=channel_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    
class ThreadsFromChannel(APIView):
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
    