from django.urls import path

from .consumer import ChatConsumer

ws_urlpatterns = [
    path("ws/",ChatConsumer.as_asgi()),
]

