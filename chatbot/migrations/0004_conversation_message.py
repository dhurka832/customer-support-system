import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_remove_conversation_message_models'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique UUID identifier for the conversation session.', primary_key=True, serialize=False)),
                ('title', models.CharField(default='New Conversation', help_text='A short summary title of the conversation subject.', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Timestamp when the conversation started.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the conversation was last updated.')),
                ('user', models.ForeignKey(help_text='The customer who initiated the conversation.', on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(help_text='The prompt or question submitted by the user.')),
                ('ai_answer', models.TextField(help_text='The response returned by the AI support model.')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Timestamp when the message exchange occurred.')),
                ('conversation', models.ForeignKey(help_text='The conversation thread this message belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatbot.conversation')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='conversation',
            index=models.Index(fields=['user', '-updated_at'], name='chatbot_con_user_id_0be7ed_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['conversation', 'created_at'], name='chatbot_mes_convers_b353f0_idx'),
        ),
    ]
