from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Belge başlığı girin'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Belge Başlığı',
            'file': 'Dosya',
        }

class DocumentVerifyForm(forms.Form):
    file = forms.FileField(
        label='Doğrulanacak Dosya',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Doğrulanacak dosyayı seçin'
    )