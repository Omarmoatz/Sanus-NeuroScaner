from django.db import models

from accounts.models import CustomUser

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messege')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messege')
    message = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'from {self.sender} to ----> {self.receiver}'