from django.db.models.signals import pre_save,post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now
from django.db.models.signals import pre_save
from .models import Message, MessageHistory ,Notification

User =  settings.AUTH_USER_MODEL

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

@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_related(sender, instance, **kwargs):
    origin = kwargs.get('origin')
    # Skip if cascade deletion already handled by a related delete
    if hasattr(origin, '__class__') and origin.__class__ is sender:
        pass  # this delete originated from user.delete()
    user = instance
    # Delete manually if any model did not use CASCADE
    Message.objects.filter(sender=user).delete()
    Message.objects.filter(receiver=user).delete()
    Notification.objects.filter(user=user).delete()
    MessageHistory.objects.filter(user=user).delete()