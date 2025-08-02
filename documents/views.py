import requests
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Document
from .forms import DocumentUploadForm, DocumentVerifyForm
import hashlib

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            
            # Pinata API'sini kullanarak dosyayı yükle
            try:
                url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                headers = {"Authorization": f"Bearer {settings.PINATA_JWT}"}

                with open(document.file.path, 'rb') as file_data:
                    files = {"file": file_data}
                    response = requests.post(url, files=files, headers=headers)
                
                if response.status_code == 200:
                    ipfs_hash = response.json()["IpfsHash"]
                    document.ipfs_hash = ipfs_hash
                    document.save()
                    messages.success(request, f'Belge başarıyla yüklendi! Hash: {document.file_hash[:16]}... IPFS: {ipfs_hash[:16]}...')
                else:
                        messages.warning(request, f'Belge yüklendi ama Pinata\'ya yüklenemedi. Status Code: {response.status_code}, Mesaj: {response.text}')
            except Exception as e:
                messages.warning(request, f'Belge yüklendi ama Pinata\'ya yüklenemedi. Hata: {e}')
            return redirect('documents:document_list')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def verify_document(request):
    if request.method == 'POST':
        form = DocumentVerifyForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            
            # Dosya hash'ini hesapla
            hash_sha256 = hashlib.sha256()
            for chunk in uploaded_file.chunks():
                hash_sha256.update(chunk)
            file_hash = hash_sha256.hexdigest()
            
            # Veritabanında ara
            try:
                existing_document = Document.objects.get(file_hash=file_hash)
                messages.success(request, f'Bu belge daha önce yüklenmiş! Yükleme tarihi: {existing_document.uploaded_at.strftime("%d/%m/%Y %H:%M")}')
            except Document.DoesNotExist:
                messages.warning(request, 'Bu belge daha önce yüklenmemiş!')
            
            return redirect('documents:verify_document')
    else:
        form = DocumentVerifyForm()
    
    return render(request, 'documents/verify.html', {'form': form})

@login_required
def document_list(request):
    documents = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'documents/list.html', {'documents': documents})