import uuid

from django.conf import settings
from django.db import models


class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} @ {self.created_at:%Y-%m-%d %H:%M}"


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique UUID identifier for the conversation session.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations',
        help_text="The customer who initiated the conversation.",
    )
    title = models.CharField(
        max_length=255,
        default="New Conversation",
        help_text="A short summary title of the conversation subject.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the conversation started.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the conversation was last updated.",
    )

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at'], name='chatbot_con_user_id_0be7ed_idx'),
        ]

    def __str__(self):
        return self.title


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation thread this message belongs to.",
    )
    question = models.TextField(help_text="The prompt or question submitted by the user.")
    ai_answer = models.TextField(help_text="The response returned by the AI support model.")
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the message exchange occurred.",
    )

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at'], name='chatbot_mes_convers_b353f0_idx'),
        ]

    def __str__(self):
        return f"Message in {self.conversation_id} @ {self.created_at:%H:%M}"
