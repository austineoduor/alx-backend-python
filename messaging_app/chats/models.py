from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.

    This allows you to add fields specific to your application without
    modifying the core Django User model.

    Attributes:
        bio (str): A short biography of the user.
        profile_picture (ImageField):  A profile picture for the user.
        location (str): The user's general location.
        website (URLField):  The user's website or blog.
        is_verified (BooleanField):  Indicates if the user's account has been verified.
    """

    bio = models.TextField(
        blank=True,  # Allow empty values in the database
        verbose_name="Biography",  # More readable in admin interface
        help_text="A short bio about yourself."  # Help text for the admin interface
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',  # Where to store images within MEDIA_ROOT
        blank=True,
        null=True,  # Allow null values in the database. Important for optional fields.
        verbose_name="Profile Picture",
        help_text="Upload a profile picture."
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Location",
        help_text="Your general location."
    )

    website = models.URLField(
        blank=True,
        verbose_name="Website",
        help_text="Your website or blog URL."
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified",
        help_text="Is the user's account verified?"
    )

    groups = models.ManyToManyField(
         Group,
         verbose_name='groups',
         blank=True,
         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
         related_name="chats_user_groups",  # <--- Add this
         related_query_name="chats_user",
     )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="chats_user_permissions",  # <--- Add this
        related_query_name="chats_user",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username  # Or self.get_full_name() if you prefer

    def get_profile_picture_url(self):
        """
        Returns the URL of the profile picture, or a default image if none is set.
        """
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return 'static/images/default_profile.png'
            

    def has_complete_profile(self):
        """
        Checks if the user has a complete profile (e.g., bio and location filled in).
        """
        return bool(self.bio and self.location)


# In models.py of another app (if you want to create a OneToOne relationship)
# from django.conf import settings
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     # ... other fields for the profile

class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    """
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        help_text="Users participating in this conversation."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the conversation was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the conversation was last updated."
    )

    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    '''
    Represents a message within a conversation
    '''
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE,
        help_text="The conversation this message belongs to."
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent the message."
    )
    text = models.TextField(
        help_text="The content of the message."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was sent."
    )

    class Meta:
        ordering = ['timestamp']

