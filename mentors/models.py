from django.db import models
from users.models import User
from startups.models import Startup

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    startups = models.ManyToManyField(Startup, related_name='mentors')  # a mentor can mentor many startups
    expertise = models.CharField(max_length=255)  # e.g., Marketing, Tech, Finance

    def __str__(self):
        return self.user.username


class ChatMessage(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"