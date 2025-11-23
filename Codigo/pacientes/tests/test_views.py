import pytest
from django.urls import reverse
from pacientes.models import Paciente, HistorialMedico

pytestmark = pytest.mark.django_db

@pytest.fixture
def paciente_existente():
    return Paciente.objects.create(
        nombre='Juan',
        apellido='Perez',
        dni='12345678',
        direccion='Calle Test',
        email='test@test.com',
        telefono='999999999',
        fechaNacimiento='1990-01-01',
        sexo='M'
    )

@pytest.fixture
def historial_existente(paciente_existente):
    return HistorialMedico.objects.create(
        paciente=paciente_existente,
        alergias='Ninguna',
        tipoSangre='O+',
        enfermedades='Ninguna'
    )

def test_submenu_pacientes(client):
    """Test vista de submenu"""
    url = reverse('pacientes:submenu_pacientes')
    response = client.get(url)
    assert response.status_code == 200

def test_historial_busqueda_get_vacio(client):
    """Test GET de búsqueda sin parámetros"""
    url = reverse('pacientes:historial_busqueda')
    response = client.get(url)
    assert response.status_code == 200
    assert 'paciente' in response.context
    assert response.context['paciente'] is None

def test_historial_busqueda_por_dni(client, paciente_existente, historial_existente):
    """Test búsqueda por DNI"""
    url = reverse('pacientes:historial_busqueda') + '?dni=12345678'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['paciente'] == paciente_existente
    assert response.context['historial'] == historial_existente

def test_historial_busqueda_por_nombre(client, paciente_existente, historial_existente):
    """Test búsqueda por nombre"""
    url = reverse('pacientes:historial_busqueda') + '?nombre=Juan'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['paciente'] == paciente_existente

def test_historial_registrar_get(client):
    """Test GET formulario de registro"""
    url = reverse('pacientes:historial_registrar')
    response = client.get(url)
    assert response.status_code == 200
    assert 'titulo' in response.context

def test_historial_registrar_post(client):
    """Test POST para registrar historial"""
    url = reverse('pacientes:historial_registrar')
    data = {
        'nombre': 'Maria',
        'apellido': 'Lopez',
        'dni': '87654321',
        'direccion': 'Av Test 123',
        'email': 'maria@test.com',
        'telefono': '888888888',
        'fecha_nacimiento': '1985-05-15',
        'genero': 'F',
        'alergias': 'Penicilina',
        'tipo_sangre': 'A+',
        'enfermedades': 'Diabetes'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Paciente.objects.filter(dni='87654321').exists()

def test_historial_actualizar_get(client, paciente_existente):
    """Test GET formulario de actualización"""
    url = reverse('pacientes:historial_actualizar', kwargs={'paciente_id': paciente_existente.id})
    response = client.get(url)
    assert response.status_code == 200

def test_historial_actualizar_post(client, paciente_existente, historial_existente):
    """Test POST para actualizar historial"""
    url = reverse('pacientes:historial_actualizar', kwargs={'paciente_id': paciente_existente.id})
    data = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'dni': '12345678',
        'direccion': 'Nueva Direccion',
        'email': 'nuevo@test.com',
        'telefono': '777777777',
        'fecha_nacimiento': '1990-01-01',
        'genero': 'M',
        'alergias': 'Polen',
        'tipo_sangre': 'O+',
        'enfermedades': 'Asma'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    paciente_existente.refresh_from_db()
    assert paciente_existente.direccion == 'Nueva Direccion'
