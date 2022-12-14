from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from ..tm03.consumers import LiveScoreConsumer

websockets = URLRouter([
    path(
        "ws/live-score/<int:game_id>", LiveScoreConsumer,
        name="live-score",
    ),
])