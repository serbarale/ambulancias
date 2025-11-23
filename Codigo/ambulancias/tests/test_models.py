# ambulancias/tests/test_models.py
import pytest
from django.db import IntegrityError
from django.utils import timezone
from ambulancias.models import Ambulancia

# Factory para generar datos de prueba
@pytest.fixture
def ambulancia_factory():
    def _create_ambulancia(placa, estado='Disponible', tipo='Tipo I', marca='Mercedes', fecha_adquisicion=timezone.now(), capacidad=4):
        return Ambulancia.objects.create(placa=placa, estado=estado, tipo=tipo, marca=marca, fecha_adquisicion=fecha_adquisicion, capacidad=capacidad)
    return _create_ambulancia

@pytest.mark.django_db
def test_tc01_registrar_ambulancia_valida(ambulancia_factory):
    # Precondición: DB vacía
    assert Ambulancia.objects.count() == 0
    
    # Pasos: Crear ambulancia válida
    ambulancia = ambulancia_factory(placa='ABC-123')
    
    # Resultado esperado: Ambulancia registrada, <5s (no medimos tiempo aquí)
    assert Ambulancia.objects.count() == 1
    assert ambulancia.placa == 'ABC-123'
    assert ambulancia.estado == 'Disponible'

@pytest.mark.django_db
def test_tc30_registrar_ambulancia_placa_duplicada(ambulancia_factory):
    # Precondición: Crear una ambulancia
    ambulancia_factory(placa='ABC-123')
    
    # Pasos: Intentar crear con placa duplicada
    with pytest.raises(IntegrityError):
        Ambulancia.objects.create(placa='ABC-123', estado='Disponible', tipo='Tipo I', marca='Mercedes', fecha_adquisicion=timezone.now(), capacidad=4)