from django.urls import path
from .views import chatbot, history, new_conversation, get_conversation, send_message_ajax

urlpatterns = [
    path("chat/", chatbot, name="chatbot"),
    path("history/", history, name="history"),
    path("conversation/new/", new_conversation, name="new_conversation"),
    path("conversation/<uuid:conversation_id>/", get_conversation, name="get_conversation"),
    path("conversation/send/", send_message_ajax, name="send_message_ajax"),
]