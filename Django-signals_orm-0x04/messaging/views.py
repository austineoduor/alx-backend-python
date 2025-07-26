#from django.contrib.auth import get_user_model
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import action
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .permissions import IsParticipantInConversation
from .models import  Conversation, Message, User
from .serializers import (ConversationSerializer,
                          MessageSerializer,
                          CreateConversationSerializer,
                          CreateMessageSerializer
                          )

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated] #Restrict to authenticated users
    search_fields = ["IsAuthenticated", "conversation_id", "Message.objects.filter", "HTTP_403_FORBIDDEN"]
    #filters,
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateConversationSerializer
        return ConversationSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned conversations to those that
        the current user is a participant in.
        """
        return Conversation.objects.filter(participants=self.request.user).distinct()


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        conv = serializer.save()
        if self.request.user not in conv.participants.all():
            conv.participants.add(self.request.user)
        return conv


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["IsAuthenticated", "conversation_id", "Message.objects.filter", "HTTP_403_FORBIDDEN"]

    def get_serializer_class(self):
        if self.action == ['create', 'update', 'partial_update']:
            return CreateMessageSerializer
        return MessageSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned messages to those
        belonging to a conversation the current user is a participant in.
        """
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id is not None:
            try:
                conversation = Conversation.objects.get(pk=conversation_id)
                if user in conversation.participants.all(): #Added check to ensure user is part of conversation
                   return Message.objects.filter(conversation=conversation)
                else:
                   return Message.objects.none() # Return empty queryset if user not in conversation
            except Conversation.DoesNotExist:
                return Message.objects.none() # Return empty queryset if conversation does not exist

        return Message.objects.filter(conversation__participants=user).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)  # Auto-assign sender to current user


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['delete'])
    def delete_user(self, request):
        user = request.user
        with transaction.atomic():
            user.delete()
        return Response({"detail": "Your account and associated data were deleted permanently."},
                        status=status.HTTP_204_NO_CONTENT)