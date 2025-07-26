from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import pre_save
from .models import Message, MessageHistory ,Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create a notification when a new message is saved.
    """
    if created:
        Notification.objects.create(
            receiving_user=instance.receiver,
            message=instance
            )


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    try:
        old_message = Message.objects.get(pk=instance.pk)  # Get the existing message
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                edited_by=instance.sender,
                message=instance,
                content=old_message.content  # Save the *old* content
            )
            instance.edited = True  # Set the 'edited' flag
    except Message.DoesNotExist:
        # It's a new message, so no history to save yet
        pass