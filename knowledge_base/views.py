from django.shortcuts import render,redirect
from .models import Document
from .forms import DocumentForm 
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
import os

@staff_member_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            document = form.save()
            from .rag import (
                load_pdf,
                split_documents,
                create_vector_store
            )
            try:
                docs = load_pdf(document.file.path)
                chunks = split_documents(docs)
                create_vector_store(chunks)
            except Exception as e:
                pass
            return redirect("document-list")
    else:
        form = DocumentForm()
    return render(request,"knowledge_base/upload_document.html",{"form":form})

def document_list(request):
    documents = Document.objects.all()
    return render(request,"knowledge_base/document_list.html",{"documents":documents})

@staff_member_required
def delete_document(request, pk):
    document = get_object_or_404(Document, id=pk)
    if request.method == "POST":
        if document.file and os.path.exists(document.file.path):
            try:
                os.remove(document.file.path)
            except Exception:
                pass
        document.delete()
        from .rag import rebuild_vector_store_from_all_docs
        rebuild_vector_store_from_all_docs()
        return redirect("document-list")
    return render(request, "knowledge_base/confirm_delete.html", {"document": document})



    