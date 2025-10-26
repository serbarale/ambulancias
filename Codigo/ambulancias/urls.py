from django.urls import path
from . import views

app_name = 'ambulancias'

urlpatterns = [
    path('', views.listar_ambulancias, name='listar_ambulancias'),
    path('registrar/', views.registrar_ambulancia, name='registrar_ambulancia'),
    path('submenu/', views.submenu_ambulancias, name='submenu_ambulancias'),
    path('editar/<int:id>/', views.editar_ambulancia, name='editar_ambulancia'),
    path("averias/", views.lista_averias, name="lista_averias"),
    path("averias/registrar/", views.registrar_averia, name="registrar_averia"),
    path("combustible/", views.lista_combustible, name="lista_combustible"),
    path("combustible/registrar/", views.registrar_combustible, name="registrar_combustible"),
    
]
