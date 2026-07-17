from django.urls import path 
from . import views

urlpatterns = [
    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("dashboard/",views.dashboard_view,name="dashboard"),
    path("profile/", views.customer_profile, name="customer_profile"),
    
    # Admin dashboard URL patterns
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/customers/", views.admin_customers, name="admin_customers"),
    path("dashboard/admin/customers/<int:user_id>/delete/", views.admin_delete_customer, name="admin_delete_customer"),
    path("dashboard/admin/customers/<int:user_id>/", views.admin_customer_detail, name="admin_customer_detail"),
    path("dashboard/admin/conversations/", views.admin_conversations, name="admin_conversations"),
    path("dashboard/admin/tickets/", views.admin_tickets, name="admin_tickets"),
    path("dashboard/admin/tickets/status/", views.admin_ticket_update_status, name="admin_ticket_update_status"),
    path("dashboard/admin/tickets/reply/", views.admin_ticket_reply, name="admin_ticket_reply"),
    path("dashboard/admin/search/", views.admin_search, name="admin_search"),
    path("dashboard/admin/export/csv/", views.export_conversations_csv, name="export_conversations_csv"),
]