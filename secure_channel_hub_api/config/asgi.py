import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from apps.channels.middleware.AuthTokenMiddleware import TokenAuthMiddleware
from apps.channels.routing import websocket_urlpatterns

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
