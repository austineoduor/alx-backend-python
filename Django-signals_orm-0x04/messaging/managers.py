from django.db import models



class UnreadMessagesManager(models.Manager):
    def unread_for(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False)