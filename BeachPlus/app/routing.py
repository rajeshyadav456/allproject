from app import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<token_user_id>\d+)/(?P<other_user_id>\d+)/(?P<chatType>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# (?P<userid>\d+)/(?P<chatType>\w+)/
#(?P<Token>\w+)/$(?P<userid>\d+)/$

