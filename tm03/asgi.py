import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import tm03.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tm03.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            tm03.routing.websocket_urlpatterns
        )
    ),
})