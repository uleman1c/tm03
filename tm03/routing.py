""" from channels.routing import ProtocolTypeRouter, URLRouter
from wsfiles.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})

 """
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/files/', consumers.FileConsumer.as_asgi()),
]

