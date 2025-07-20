import re
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Document
from .forms import DocumentUploadForm, DocumentVerifyForm
import hashlib

@login_required
#Giriş yapmış kullanıcı dosya yükler.
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by  = request.user
            document.save()

            if document.file_hash:
                messages.success(request, 'Dosya başarıyla yüklendi.')
            else:
                messages.error(request, 'Dosya hash hesaplanırken bir hata oluştu.')
            return redirect('document_list')

    else:
        form = DocumentUploadForm()

    return render(request, 'documents/upload.html', {'form': form})


@login_required
def verify_document(request):
    if request.method == 'POST':
        form = DocumentVerifyForm((request.POST, request.FILES))
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            
            hash_sha256 = hashlib.sha256()
            for chunk in uploaded_file.chunks():
                hash_sha256.update(chunk)

            file_hash = hash_sha256.hexdigest()

            try:
                existing_document = Document.objects.get(file_hash=file_hash)
                messages.success(request, f'Bu belge daha önce yüklenmiş! Yükleme tarihi: {existing_document.uploaded_at.strftime("%d/%m/%Y %H:%M")}')
            except Document.DoesNotExist:
                messages.warning(request, 'Bu belge henüz yüklenmemiş!')

            return redirect('verify_document')

    else:
        form = DocumentVerifyForm()

    return render(request, 'documents/verify.html', {'form': form})


@login_required
def document_list(request):
    documents = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'documents/list.html', {'documents': documents})