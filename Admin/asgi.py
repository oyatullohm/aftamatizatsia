import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

# Agar consumers fayling bo‘lsa
from .consumers import KitchenOrderConsumer


application = ProtocolTypeRouter({
    "http": django_asgi_app,

    # WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/kitchen/<int:department_id>/", KitchenOrderConsumer.as_asgi()),
        ])
    ),
})
