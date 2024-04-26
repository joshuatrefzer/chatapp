from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.http import HttpRequest
from .models import Channel, Message, Thread

@receiver(pre_save, sender=Channel)
def delete_previous_picture(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.picture != instance.picture:
                if old_instance.picture:
                    default_storage.delete(old_instance.picture.path)
        except sender.DoesNotExist:
            pass 
        
@receiver(pre_save, sender=Channel)
def check_empty_members(sender, instance, **kwargs):
    # Überprüfen, ob die Anfrage eine PATCH- oder PUT-Anfrage ist
    if isinstance(kwargs.get('request'), HttpRequest) and kwargs['request'].method in ['PATCH', 'PUT']:
        # Wenn es sich um eine PATCH- oder PUT-Anfrage handelt und members leer sind, lösche die Instanz
        if not instance.members.exists():
            instance.delete()


@receiver(pre_delete, sender=Channel)
def delete_channel_picture(sender, instance, **kwargs):
    if instance.picture:
        default_storage.delete(instance.picture.path)
    

@receiver(pre_delete, sender=Message)
def delete_message_attachments(sender, instance, **kwargs):
    if instance.attachment:
        default_storage.delete(instance.attachment.path)

@receiver(pre_delete, sender=Thread)
def delete_thread_attachments(sender, instance, **kwargs):
    if instance.attachment:
        default_storage.delete(instance.attachment.path)