import pytest
from django.core.exceptions import ValidationError
from emergencias.models import InformeEmergencia
from ambulancias.models import Ambulancia

pytestmark = pytest.mark.django_db

@pytest.fixture
def ambulancia():
    return Ambulancia.objects.create(
        placa="UT-TEST-01",
        estado="Disponible",
        tipo="Tipo I",
        marca="Test",
        fecha_adquisicion="2024-01-01",
        capacidad=4
    )

def test_tc02_crear_informe_valido(ambulancia):
    """TC-02: Registrar informe completo con datos válidos"""
    informe = InformeEmergencia(
        ambulancia=ambulancia,
        direccion="Av. Test 123, Lima",  # Changed from direccion_emergencia
        prioridad="alta",
        estado="pendiente",
        nombre_chofer="Test Driver"
    )
    informe.full_clean()
    informe.save()
    assert InformeEmergencia.objects.count() == 1

def test_tc31_informe_ubicacion_invalida(ambulancia):
    """TC-31: Validar rechazo de ubicación inválida"""
    informe = InformeEmergencia(
        ambulancia=ambulancia,
        direccion="",  # Changed from direccion_emergencia
        prioridad="alta",
        estado="pendiente",
        nombre_chofer="Test Driver"
    )
    with pytest.raises(ValidationError):
        informe.full_clean()