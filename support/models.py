from django.db import models
from django.contrib.auth.models import User 

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ["Low","LOw"],
        ["Medium","Medium"],
        ["High","High"]
    ]

    STATUS_cHOICES = [
        ["Open","Open"],
        ["In Progress","In Progress"],
        ["Closed","Closed"]
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20,choices=STATUS_cHOICES,default="Open")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to {self.ticket.title} by {self.replied_by.username}"

