from django.shortcuts import render

from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import  status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer
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
            user_token.delete()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Token not provided."}, status=status.HTTP_400_BAD_REQUEST)