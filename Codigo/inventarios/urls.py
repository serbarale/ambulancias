from django.urls import path
from . import views

app_name = 'inventarios'

urlpatterns = [
    path("submenu/", views.submenu_inventarios, name="submenu_inventarios"),
    path("checklist/buscar/", views.buscar_ambulancia_checklist, name="buscar_ambulancia_checklist"),
    path("checklist/historial/<int:ambulancia_id>/", views.historial_checklist, name="historial_checklist"),
    path("checklist/registrar/<int:ambulancia_id>/", views.registrar_checklist, name="registrar_checklist"),
    path("checklist/editar/<int:checklist_id>/", views.editar_checklist, name="editar_checklist"),
    path("insumos/", views.listar_insumos, name="listar_insumos"),
    path("insumos/registrar/", views.registrar_insumo, name="registrar_insumo"),
    path("insumos/editar/<int:insumo_id>/", views.editar_insumo, name="editar_insumo"),
    path("insumos/eliminar/<int:insumo_id>/", views.eliminar_insumo, name="eliminar_insumo"),
]

