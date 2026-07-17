from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Conversation, Message, ChatHistory
from knowledge_base.rag import generate_answer


@login_required
def chatbot(request):
    conversations = Conversation.objects.filter(user=request.user)
    active_conv = conversations.first()
    if not active_conv:
        active_conv = Conversation.objects.create(
            user=request.user,
            title="Welcome Chat",
        )
        conversations = Conversation.objects.filter(user=request.user)

    return render(
        request,
        "chatbot/chatbot.html",
        {
            "conversations": conversations,
            "active_conv": active_conv,
        }
    )


@login_required
def new_conversation(request):
    Conversation.objects.create(
        user=request.user,
        title="New Chat Session",
    )
    return redirect("chatbot")


@login_required
def get_conversation(request, conversation_id):
    try:
        conv = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        raise Http404("Conversation not found")

    messages = [
        {
            "question": m.question,
            "ai_answer": m.ai_answer,
            "created_at": m.created_at.strftime('%H:%M'),
        }
        for m in conv.messages.all()
    ]

    return JsonResponse({
        'success': True,
        'conversation_id': str(conv.id),
        'title': conv.title,
        'messages': messages
    })


@login_required
def send_message_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            conversation_id = data.get('conversation_id')
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({'success': False, 'error': 'Empty question'}, status=400)

            try:
                conv = Conversation.objects.get(id=conversation_id, user=request.user)
            except (Conversation.DoesNotExist, ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Conversation not found'}, status=404)

            answer = generate_answer(question)

            ChatHistory.objects.create(user=request.user, question=question, answer=answer)

            msg = Message.objects.create(
                conversation=conv,
                question=question,
                ai_answer=answer,
            )

            title = conv.title
            if title in ("New Chat Session", "Welcome Chat"):
                title = question[:45] + '...' if len(question) > 45 else question

            conv.title = title
            conv.save(update_fields=["title", "updated_at"])

            return JsonResponse({
                'success': True,
                'question': msg.question,
                'ai_answer': msg.ai_answer,
                'created_at': msg.created_at.strftime('%H:%M'),
                'conv_title': title
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def history(request):
    chats = ChatHistory.objects.filter(user=request.user)
    return render(request, "chatbot/history.html", {"chats": chats})
