import os

# Set Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatProject.settings')

# Import Django and channels components
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Get the ASGI application first
django_asgi_app = get_asgi_application()

# Then import your websocket patterns
from chat.routing import websocket_urlpatterns

# Define the application
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)