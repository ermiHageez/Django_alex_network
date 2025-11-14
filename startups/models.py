from django.db import models
from users.models import User

class Startup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='startups')
    members = models.ManyToManyField(User, related_name='member_startups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
