from django.urls import re_path
from .consumer import VideoConsumer

wt_urlpattern = [
    re_path(r'ws/video/',VideoConsumer.as_asgi()),
]