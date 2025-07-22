from django.db import models
from django.contrib.auth.models import User
import hashlib
import os


class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_hash = models.CharField(max_length=64, blank=True)
    file_size = models.IntegerField(default=0)
    ipfs_hash = models.CharField(max_length=100, blank=True)
    blockchain_tx = models.CharField(max_length=100, blank=True)


    def save(self, *args, **kwargs):
        # Dosya hash'ini hesapla
        if self.file and not self.file_hash:
            self.file_hash = self.calculate_hash()
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def calculate_hash(self):
        """Dosyanın SHA-256 hash'ini hesaplar"""
        hash_sha256 = hashlib.sha256()
        for chunk in self.file.chunks():
            hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def __str__(self):
        return f"{self.title} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"