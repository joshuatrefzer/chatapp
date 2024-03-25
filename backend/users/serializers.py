from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'picture', 'is_online', 'password']  # Füge hier weitere erforderliche Felder hinzu
        extra_kwargs = {'password': {'write_only': True}}  # Das Passwort sollte nur zum Schreiben verwendet werden