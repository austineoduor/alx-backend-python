from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Message,Notification

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a new message is saved.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)