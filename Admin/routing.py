# your_app/routing.py
from django.urls import re_path
from .consumers import KitchenOrderConsumer

websocket_urlpatterns = [
    re_path(r"ws/printer/(?P<department_id>\d+)/$", KitchenOrderConsumer.as_asgi()),

]
