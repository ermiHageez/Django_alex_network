# startups/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/mentor/(?P<mentor_id>\d+)/$', consumers.MentorChatConsumer.as_asgi()),
]
