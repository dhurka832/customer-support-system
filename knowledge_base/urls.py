from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.document_list,name="document-list"),
    path("upload/",views.upload_document,name="upload-document"),
    path("delete/<int:pk>/",views.delete_document,name="delete-document"),
]
