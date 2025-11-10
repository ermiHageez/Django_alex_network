from django.db import models
from users.models import User

class Startup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='startups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
