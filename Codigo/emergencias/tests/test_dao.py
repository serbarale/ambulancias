import pytest
from django.core.exceptions import ValidationError
from ambulancias.models import Ambulancia
from emergencias.dao.informe_dao import InformeEmergenciaDAO

pytestmark = pytest.mark.django_db

@pytest.fixture
def ambulancia():
    return Ambulancia.objects.create(
        placa="UT-DAO-01",
        estado="Disponible",
        tipo="Tipo I",
        marca="DAO Test",
        fecha_adquisicion="2024-01-01",
        capacidad=4
    )

def test_dao_crear_obtener_listar(ambulancia):
    dao = InformeEmergenciaDAO()
    data = {
        "ambulancia": ambulancia,
        "direccion": "Av. DAO Test 123",
        "prioridad": "alta",
        "estado": "pendiente",
        "nombre_chofer": "DAO Driver"
    }
    
    created = dao.crear(data)
    assert created.id is not None
    
    retrieved = dao.obtener_por_id(created.id)
    assert retrieved.direccion == data["direccion"]