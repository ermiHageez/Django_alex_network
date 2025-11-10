from django.db import models
from users.models import User

class Investor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investors')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
