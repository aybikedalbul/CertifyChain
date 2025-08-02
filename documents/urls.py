from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.home, name='home'),
    path('documents/', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('verify/', views.verify_document, name='verify_document'),
]