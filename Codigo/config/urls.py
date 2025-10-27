"""
URL configuration for ambulancias project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ambulancias/', include('ambulancias.urls')),
    path('emergencias/', include('emergencias.urls')),
    path('pacientes/', include('pacientes.urls')),
]
