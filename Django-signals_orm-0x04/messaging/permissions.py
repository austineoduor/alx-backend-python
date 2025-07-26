from .models import Conversation, Message
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantInConversation(BasePermission):
    """
    Permission to allow only participants in a conversation to send, view, update and delete messages.
    """
    # Check if user is authenticated
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user        

# class IsSenderOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Allow safe methods for participants
#         if request.method in SAFE_METHODS:
#             return request.user in obj.conversation.participants.all()
#         # Only sender can modify
#         return obj.sender == request.user