from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ambulancias/', include('ambulancias.urls')),
    path('emergencias/', include('emergencias.urls')),
    path('inventarios/', include('inventarios.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('', include('core.urls')),
]