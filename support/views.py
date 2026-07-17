from django.shortcuts import render,redirect
from .models import Ticket
from .forms import TicketForm
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request,"support/ticket_list.html",{"tickets":tickets})

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user 
            ticket.save()
    
            try:
                from django.contrib.auth.models import User
                from django.core.mail import send_mail
                
                admin_emails = list(User.objects.filter(is_staff=True).exclude(email='').values_list('email', flat=True))
                if admin_emails:
                    subject = f"New Support Ticket: {ticket.title}"
                    message = f"Hello Team,\n\nCustomer '{request.user.username}' has submitted a new support ticket.\n\nTicket: {ticket.title}\nPriority: {ticket.priority}\n\nDescription:\n{ticket.description}\n\nPlease check the admin portal to update status and reply.\n\nBest regards,\nSupportSphere System"
                    send_mail(
                        subject,
                        message,
                        'support@example.com',
                        admin_emails,
                        fail_silently=True
                    )
            except Exception:
                pass
                
            return redirect("ticket-list")
    else:
        form = TicketForm()
    return render(request,"support/create_ticket.html",{"form":form})


@login_required
def update_ticket(request,pk):
    ticket = get_object_or_404(Ticket,id=pk,created_by=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST,instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket-list")
    else:
        form = TicketForm(instance=ticket)
    return render(request,"support/update_ticket.html",{"form":form})

@login_required
def delete_ticket(request,pk):
    ticket = get_object_or_404(Ticket,id=pk,created_by=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("ticket-list")
    return render(request,"support/delete_ticket.html",{"ticket":ticket})

