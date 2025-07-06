from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, Message

User = get_user_model()  # Important: Use get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name') # Added more fields
        read_only_fields = ('id',)  # Prevent ID modification


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User serializer
    # conversation = serializers.PrimaryKeyRelatedField(read_only=True) #Or StringRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'text', 'timestamp')
        read_only_fields = ('id', 'sender', 'timestamp') #timestamp is often set automatically


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested User serializer
    messages = MessageSerializer(many=True, read_only=True)  # Nested Message serializer

    class Meta:
        model = Conversation
        fields = ('id', 'participants', 'messages', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


#Serializers for creating conversations and Messages

class CreateConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Conversation
        fields = ('participants',)

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('conversation', 'sender')


class CreateMessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True) #added to ensure text is a required field

    class Meta:
        model = Message
        fields = ('conversation', 'text')