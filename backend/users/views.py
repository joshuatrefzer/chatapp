from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import  status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, ChatUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

# Create your views here.
CustomUser = get_user_model()

@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = CustomUserSerializer(user)
    user.is_online = True
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def logout(request):
    token = request.data.get('token')
    
    if token:
        user_token = Token.objects.filter(key=token).first()
        
        if user_token:
            user = user_token.user
            user_token.delete()
            user.is_online = False
            user.save()
            
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Token not provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def upload_profile_image(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if 'picture' not in request.data:
        return Response({"error": "Profile picture is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.picture:
        user.picture.delete()
        
    user.picture = request.data['picture']
    user.save()
    
    serializer = CustomUserSerializer(user, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class ChatUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(is_superuser=False)
    serializer_class = ChatUserSerializer

    def list(self, request, *args, **kwargs):
        if request.method != 'GET':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)