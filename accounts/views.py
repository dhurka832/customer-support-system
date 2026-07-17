from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
import json
import csv
from .forms import RegisterForm
from chatbot.models import Conversation, Message
from support.models import Ticket

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_staff

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def dashboard_view(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
    return redirect("chatbot")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    today = timezone.now().date()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    total_users = User.objects.filter(is_staff=False).count()
    total_conversations = Conversation.objects.count()
    total_messages = Message.objects.count()
    active_users_today = (
        Conversation.objects.filter(updated_at__date=today)
        .values('user_id').distinct().count()
    )

    if total_users > 0:
        avg_conversations = round(total_conversations / total_users, 2)
        avg_messages = round(total_messages / total_users, 2)
    else:
        avg_conversations = 0.00
        avg_messages = 0.00

    latest_customers = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    recent_conversations = (
        Conversation.objects.select_related('user').order_by('-created_at')[:5]
    )

    conv_timeline = list(
        Conversation.objects.filter(created_at__gte=thirty_days_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    msg_timeline = list(
        Message.objects.filter(created_at__gte=thirty_days_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    conv_labels = [e['date'].strftime('%b %d') for e in conv_timeline]
    conv_data = [e['count'] for e in conv_timeline]
    
    msg_dict = {e['date'].strftime('%b %d'): e['count'] for e in msg_timeline}
    msg_data = [msg_dict.get(label, 0) for label in conv_labels]

    context = {
        'total_users': total_users,
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'active_users_today': active_users_today,
        'avg_conversations': avg_conversations,
        'avg_messages': avg_messages,
        'latest_customers': latest_customers,
        'recent_conversations': recent_conversations,
        'conv_labels_json': json.dumps(conv_labels),
        'conv_data_json': json.dumps(conv_data),
        'msg_data_json': json.dumps(msg_data),
        'today_date': today,
    }

    return render(request, 'dashboard/home.html', context)


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_customers(request):
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'date_joined')
    direction = request.GET.get('dir', 'desc')

    queryset = User.objects.filter(is_staff=False)

    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    users_list = list(
        queryset.annotate(
            total_conversations=Count('conversations', distinct=True),
            total_messages=Count('conversations__messages', distinct=True),
        )
    )

    if sort_by == 'name':
        users_list.sort(key=lambda u: (u.first_name or '').lower(), reverse=(direction == 'desc'))
    elif sort_by == 'email':
        users_list.sort(key=lambda u: (u.email or '').lower(), reverse=(direction == 'desc'))
    elif sort_by == 'conversations':
        users_list.sort(key=lambda u: u.total_conversations, reverse=(direction == 'desc'))
    elif sort_by == 'messages':
        users_list.sort(key=lambda u: u.total_messages, reverse=(direction == 'desc'))
    else: 
        users_list.sort(key=lambda u: u.date_joined, reverse=(direction == 'desc'))

    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/customers.html', {
        'page_obj': page_obj,
        'current_sort': sort_by,
        'current_dir': direction,
        'search_query': search_query
    })


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_customer_detail(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    conversation_list = list(
        Conversation.objects.filter(user_id=user_id)
        .order_by('-created_at')
        .prefetch_related('messages')
    )
    for conv in conversation_list:
        # Template iterates `conv.messages` directly (no `.all`), so materialize it here.
        conv.messages = list(conv.messages.all())

    paginator = Paginator(conversation_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/customer_detail.html', {
        'customer': customer,
        'page_obj': page_obj
    })


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_conversations(request):
    search_query = request.GET.get('q', '').strip()
    date_filter = request.GET.get('date_filter', 'all').lower()

    conversation_qs = Conversation.objects.select_related('user').prefetch_related('messages').order_by('-created_at')

    if date_filter and date_filter != 'all':
        now = timezone.now()
        target_date = None
        if date_filter == 'today':
            target_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_filter == '7days':
            target_date = now - timedelta(days=7)
        elif date_filter == '30days':
            target_date = now - timedelta(days=30)
        if target_date:
            conversation_qs = conversation_qs.filter(created_at__gte=target_date)

    if search_query:
        conversation_qs = conversation_qs.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(messages__question__icontains=search_query) |
            Q(messages__ai_answer__icontains=search_query)
        ).distinct()

    conversation_list = conversation_qs

    paginator = Paginator(conversation_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/conversations.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'date_filter': date_filter
    })


@login_required
@user_passes_test(is_admin, login_url='login')
def export_conversations_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="support_conversations.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Email', 'Question', 'AI Answer', 'Timestamp'])

    message_logs = (
        Message.objects.select_related('conversation__user')
        .order_by('-created_at')
        .iterator()
    )

    for msg in message_logs:
        user = msg.conversation.user
        if user:
            customer_name = user.get_full_name() or user.username
            email = user.email
        else:
            customer_name = "Unknown"
            email = ""
        writer.writerow([
            customer_name,
            email,
            msg.question,
            msg.ai_answer,
            msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_tickets(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all').lower()
    priority_filter = request.GET.get('priority', 'all').lower()

    queryset = Ticket.objects.select_related('created_by').order_by('-created_at')

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(created_by__username__icontains=search_query) |
            Q(created_by__email__icontains=search_query)
        )

    status_map = {'open': 'Open', 'in_progress': 'In Progress', 'closed': 'Closed'}
    if status_filter in status_map:
        queryset = queryset.filter(status=status_map[status_filter])

    priority_map = {'low': 'Low', 'medium': 'Medium', 'high': 'High'}
    if priority_filter in priority_map:
        queryset = queryset.filter(priority=priority_map[priority_filter])

    total_count = Ticket.objects.count()
    open_count = Ticket.objects.filter(status='Open').count()
    in_progress_count = Ticket.objects.filter(status='In Progress').count()
    closed_count = Ticket.objects.filter(status='Closed').count()

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/tickets.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'total_count': total_count,
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'closed_count': closed_count,
    })


@login_required
def customer_profile(request):
    from support.models import Ticket
    from .forms import ProfileUpdateForm
    
    total_conversations = Conversation.objects.filter(user=request.user).count()
    total_messages = Message.objects.filter(conversation__user=request.user).count()
    total_tickets = Ticket.objects.filter(created_by=request.user).count()
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("customer_profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request, "accounts/profile.html", {
        "form": form,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_tickets": total_tickets
    })


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_delete_customer(request, user_id):
    if request.method == "POST":
        customer = get_object_or_404(User, id=user_id, is_staff=False)
        customer.delete()
    return redirect("admin_customers")


from django.http import JsonResponse

@login_required
@user_passes_test(is_admin, login_url='login')
def admin_ticket_update_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ticket_id = data.get('ticket_id')
            new_status = data.get('status')
            ticket = get_object_or_404(Ticket, id=ticket_id)
            
            status_choices = dict(Ticket.STATUS_cHOICES)
            if new_status in status_choices:
                ticket.status = new_status
                ticket.save()
                return JsonResponse({'success': True, 'status': ticket.status})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


from django.core.mail import send_mail
from support.models import TicketReply

@login_required
@user_passes_test(is_admin, login_url='login')
def admin_ticket_reply(request):
    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
        reply_body = request.POST.get('body', '').strip()
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if reply_body:
            TicketReply.objects.create(
                ticket=ticket,
                replied_by=request.user,
                body=reply_body
            )
            try:
                subject = f"Support Ticket Update: {ticket.title}"
                message = f"Hello {ticket.created_by.username},\n\nAn admin has replied to your support ticket '{ticket.title}'.\n\nReply:\n{reply_body}\n\nView details in your support portal.\n\nBest regards,\nSupportSphere Team"
                send_mail(
                    subject,
                    message,
                    'support@example.com',
                    [ticket.created_by.email],
                    fail_silently=True
                )
            except Exception:
                pass
        return redirect("admin_tickets")
    return redirect("admin_tickets")


@login_required
@user_passes_test(is_admin, login_url='login')
def admin_search(request):
    q = request.GET.get('q', '').strip()
    users = []
    conversations = []
    tickets = []
    
    if q:
        users = User.objects.filter(is_staff=False).filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )[:10]
        conversations = Conversation.objects.select_related('user').filter(
            Q(user__username__icontains=q) |
            Q(user__email__icontains=q) |
            Q(title__icontains=q) |
            Q(messages__question__icontains=q) |
            Q(messages__ai_answer__icontains=q)
        ).distinct().order_by('-created_at')[:10]
        tickets = Ticket.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(created_by__username__icontains=q)
        ).distinct().select_related('created_by')[:10]
        
    return render(request, "dashboard/search_results.html", {
        "global_search_query": q,
        "users": users,
        "conversations": conversations,
        "tickets": tickets
    })
