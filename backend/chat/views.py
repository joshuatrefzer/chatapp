from django.shortcuts import render
from rest_framework import viewsets, status
from django.db.models import Q
from users.serializers import CustomUserSerializer, ChatUserSerializer
from users.models import CustomUser
from .models import Channel, Message, Thread
from .serializers import ChannelSerializer, MessageSerializer, ThreadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    

class ChannelViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
class ThreadViewset(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    

#austesten (Müsste nun geordnet sein nach Zeit) #auch thread Nachrichten sollen zurückkommen?? 
class Messages_and_Thread_from_Channel(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, channel_id, format=None):
        messages = Message.objects.filter(source=channel_id).order_by('created_at')
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
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
            'preview_messages': message_serializer.data  
        }
        return Response(data)
    
    
    
class ThreadsFromMessages(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, message_id, format=None):
        threads = Thread.objects.filter(source=message_id)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)
    
    
class ChannelsForUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        channels = Channel.objects.filter(members=user)
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)
    
        


class SearchAll(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        search_value = request.data.get('search_value')
        chats = request.data.get('chats')
        user_id = request.data.get('current_user') 
        
        if search_value and user_id:  
            channels_from_user = Channel.objects.filter(members=user_id)
            channels_filter = channels_from_user.filter(name__icontains=search_value)
            
            messages_from_user = Message.objects.filter(source__in=chats) 
            messages_filter = messages_from_user.filter(content__icontains=search_value)
            filtered_message_ids = [msg.id for msg in messages_from_user]
            
            threads = Thread.objects.filter(content__icontains=search_value, source__in=filtered_message_ids)
            
            users = CustomUser.objects.filter(username__icontains=search_value) \
                                       .exclude(is_superuser=True) | \
                    CustomUser.objects.filter(email__icontains=search_value) \
                                     .exclude(is_superuser=True)
            
            channel_serializer = ChannelSerializer(channels_filter, many=True)
            message_serializer = MessageSerializer(messages_filter, many=True)
            thread_serializer = ThreadSerializer(threads, many=True)
            user_serializer = ChatUserSerializer(users, many=True)
            
            data = {
                'channels': channel_serializer.data,
                'messages': message_serializer.data,
                'threads': thread_serializer.data,
                'users': user_serializer.data
            }
            
            return Response(data)
        else:
            
            return Response({'error': 'Search value cannot be empty'}, status=400)
    
class SearchUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        search_value = request.data.get('search_value')
        
        if search_value:
            users = CustomUser.objects.filter(username__icontains=search_value) \
                                       .exclude(is_superuser=True)
            users |= CustomUser.objects.filter(email__icontains=search_value) \
                                       .exclude(is_superuser=True)
            
            user_serializer = ChatUserSerializer(users, many=True)
            
            data = {
                'users': user_serializer.data
            }
            
            return Response(data)
            
        else:
            return Response({'error': 'Search value cannot be empty'}, status=400)