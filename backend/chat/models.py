from django.conf import settings
import uuid
from django.db import models
import json



from users.models import CustomUser


class Channel(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  
    members = models.ManyToManyField(CustomUser, related_name='channels')
    is_channel = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='channel_pictures/', null=True, blank=True)
    read_by = models.ManyToManyField(CustomUser, related_name='read_channels', blank=True)
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField() #Muss Charfield 
    created_at = models.DateTimeField(auto_now_add=True) 
    source = models.ForeignKey(Channel , on_delete=models.CASCADE)
    reactions = models.JSONField(blank=True, default=list)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)
    
    def __str__(self):
        return f"Message from {self.author} at {self.created_at}"
    
        
class Thread(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Message , on_delete=models.CASCADE)
    reactions = models.JSONField(blank=True, default=list)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)
    
    def __str__(self):
        return f"Message from {self.author} at {self.created_at}"
    
        
    

    
    