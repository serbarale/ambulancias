from django.urls import path
from . import views

app_name = 'emergencias'

urlpatterns = [
    path('informes/', views.listar_informes_emergencia, name='listar_informes_emergencia'),
    path('informes/registrar/<int:ambulancia_id>/',views.registrar_informe, name='registrar_informe'),
    path("informes/pacientes/", views.listar_informes_desde_pacientes, name="lista_informes_pacientes"),
    path('informes/asignar/', views.asignar_ambulancia, name='asignar_ambulancia'),
    path("informes/registrar/", views.registrar_informe, name="registrar_informe"),
    path("informes/<int:informe_id>/detalles/", views.detalles_informe, name="detalles_informe"),
    path("informes/<int:id>/revocacion/", views.generar_revocacion, name="generar_revocacion"),
    path("informes/<int:id>/consentimiento/", views.generar_consentimiento, name="generar_consentimiento"),
    path("informes/<int:id>/reporte/", views.generar_reporte_emergencia, name="generar_reporte_emergencia"),
]