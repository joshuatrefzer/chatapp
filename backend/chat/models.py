from django.db import models
from users.models import CustomUser


# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name='channels')
    is_channel = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='channel_pictures/', null=True, blank=True)
    read_by = models.ManyToManyField(CustomUser, related_name='read_channels', blank=True)
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Channel , on_delete=models.CASCADE)
    reactions = models.ManyToManyField(CustomUser, related_name='message_reactions')
    
    def __str__(self):
        return f"Message from {self.author} at {self.created_at}"
    
    
class Thread(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Message , on_delete=models.CASCADE)
    reactions = models.ManyToManyField(CustomUser, related_name='thread_reactions')
    
    def __str__(self):
        return f"Message from {self.author} at {self.created_at}"
    
        
    

    
    