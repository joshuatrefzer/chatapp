from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'picture', 'is_online']  
        extra_kwargs = {'password': {'write_only': True}}  
        
    def get_picture(self, obj):
        if obj.picture:
            return self.context['request'].build_absolute_uri(obj.picture.url)
        return None
