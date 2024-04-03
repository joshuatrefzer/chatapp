from django.contrib import admin
from .models import Channel, Message, Thread

# Register your models here.
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_channel' , 'hash' )
    filter_horizontal = ('members', 'read_by')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'source')
    filter_horizontal = ('reactions',)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at', 'source')
    filter_horizontal = ('reactions',)

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Thread, ThreadAdmin)