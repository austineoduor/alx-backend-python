# from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    Message, Conversation,
    User, Notification, MessageHistory
    )

# User = get_user_model()  # or Important: Use get_user_model()

#["serializers.SerializerMethodField()", "serializers.ValidationError"]

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'phone_number', 'password', 'last_name')
        read_only_fields = ('user_id',)  # Prevent ID modification


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    message_id = serializers.UUIDField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    message_preview = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ('message_id','parent_message', 'content', 'receiver','sender','timestamp','message_preview')
        read_only_fields = fields #timestamp is often set automatically
    def get_message_preview(self, obj):
        text = obj.content or ""
        return text[:100] + ("…" if len(text) > 100 else "")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested User serializer
    messages = MessageSerializer(many=True, read_only=True)  # Nested Message serializer

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'messages', 'created_at', 'updated_at')
        read_only_fields = fields


#Serializers for creating conversations

class CreateConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=User.objects.all()
        )
    class Meta:
        model = Conversation
        fields = ('participants',)

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation

    def update(self, instance, validated_data):
        users = validated_data.get('participants')
        if users is not None:
            instance.participants.set(users)
        instance.save()
        return instance

#Serializers for creating Messagess
class CreateMessageSerializer(serializers.ModelSerializer):
    content  = serializers.CharField(required=True, help_text="The content of the message.") #added to ensure text is a required field

    class Meta:
        model = Message
        fields = ('__all__')

    def update(self, instance, validated_data):
        # Only allow editing content field
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class NoficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        field = '__all__'
        read_only_fields = ('__all__',)


class MessageHistorySerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)
    timestamp = serializers.DateTimeField(read_only=True)
    class Meta:
        model = MessageHistory
        field = '__all__'
        read_only_fields = '__all__'

class RecursiveReplySerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'receiver', 'content', 'timestamp', 'replies')

    def get_replies(self, obj):
        # Assumes replies are already prefetched
        return RecursiveReplySerializer(
            obj.replies.all(), 
            many=True, 
            context=self.context
        ).data