from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'file_hash', 'file_size')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('title', 'file_hash')
    readonly_fields = ('file_hash', 'file_size', 'uploaded_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('uploaded_by')