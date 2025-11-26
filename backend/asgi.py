import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Initialize Django ASGI application first (this calls django.setup())
django_asgi_app = get_asgi_application()

# Import routing after Django is initialized to avoid AppRegistryNotReady
import startups.routing
import mentors.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            startups.routing.websocket_urlpatterns + mentors.routing.websocket_urlpatterns
        )
    ),
})
