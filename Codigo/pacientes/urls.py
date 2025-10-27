from django.urls import path
from . import views

urlpatterns = [
    path('submenu/', views.submenu, name='submenu_pacientes'),
    path('historial/', views.historial_busqueda, name='historial_busqueda'),
    path('historial/registrar/', views.historial_registrar, name='historial_registrar'),
    path('historial/actualizar/<int:paciente_id>/', views.historial_actualizar, name='historial_actualizar'),
]
