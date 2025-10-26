import pytest
from django.urls import reverse
from django.test import Client
from ambulancias.models import Ambulancia

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db 
def test_tc01_registrar_ambulancia_valida_via_view(client):
    assert Ambulancia.objects.count() == 0
    
    url = reverse('ambulancias:registrar_ambulancia')
    data = {
        'placa': 'DEF-456',
        'estado': 'Disponible',
        'tipo': 'Tipo I',
        'marca': 'Ford', 
        'fecha_adquisicion': '2025-01-01',
        'capacidad': 5
    }
    response = client.post(url, data)
    
    assert response.status_code == 302
    assert Ambulancia.objects.count() == 1
    assert Ambulancia.objects.first().placa == 'DEF-456'