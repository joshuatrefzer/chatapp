from django.shortcuts import render
from rest_framework import viewsets
from .models import Channel, Message
from .serializers import ChannelSerializer, MessageSerializer, ThreadSerializer
from rest_framework.views import APIView


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    
    
class ThreadViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = ThreadSerializer