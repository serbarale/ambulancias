# ambulancias/tests/test_dao.py
import pytest
from django.utils import timezone
from ambulancias.dao import AmbulanciaDAO
from ambulancias.models import Ambulancia

@pytest.mark.django_db
def test_dao_create_ambulancia_valida():
    # Precondición: DB vacía
    assert Ambulancia.objects.count() == 0
    
    # Pasos: Usar DAO para crear
    ambulancia = AmbulanciaDAO.create(placa='XYZ-789', estado='Disponible', tipo='Tipo I', marca='Toyota', fecha_adquisicion=timezone.now(), capacidad=6)
    
    # Resultado esperado
    assert Ambulancia.objects.count() == 1
    assert ambulancia.placa == 'XYZ-789'