from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.ticket_list,name="ticket-list"),
    path('create/',views.create_ticket,name="create-ticket"),
    path('update/<int:pk>/',views.update_ticket,name="update-ticket"),
    path('delete/<int:pk>/',views.delete_ticket,name="delete-ticket")
]
