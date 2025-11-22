# startups/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/startup/(?P<startup_id>\d+)/$', consumers.StartupChatConsumer.as_asgi()),
]
