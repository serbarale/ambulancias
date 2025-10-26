import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ambulancias.models import Ambulancia

pytestmark = pytest.mark.django_db

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def client_logged(client, user):
    client.force_login(user)
    return client

@pytest.fixture
def ambulancia():
    return Ambulancia.objects.create(
        placa="UT-VIEW-01",
        estado="Disponible",
        tipo="Tipo I",
        marca="View Test",
        fecha_adquisicion="2024-01-01",
        capacidad=4
    )

def test_registrar_informe_post(client_logged, ambulancia):
    """Prueba POST con datos válidos"""
    url = reverse("emergencias:registrar_informe", 
                 kwargs={"ambulancia_id": ambulancia.id})
    data = {
        "direccion": "Av. View Test 123",
        "prioridad": "alta",
        "estado": "pendiente",
        "nombre_chofer": "View Driver"
    }
    response = client_logged.post(url, data)
    assert response.status_code == 302 

def test_listar_informes_get(client_logged):
    """Prueba GET de listado de informes"""
    url = reverse("emergencias:listar_informes_emergencia")
    response = client_logged.get(url)
    assert response.status_code == 200
    assert "informes" in response.context
    assert "prioridades" in response.context
    expected_prioridades = dict([
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja')
    ])
    assert response.context["prioridades"] == expected_prioridades