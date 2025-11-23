# ambulancias/tests/test_dao.py
import pytest
from django.utils import timezone
from ambulancias.dao import AmbulanciaDAO
from ambulancias.dao.averia_dao import AveriaDAO
from ambulancias.dao.combustible_dao import CombustibleDAO
from ambulancias.models import Ambulancia, Avería, Combustible
from datetime import date

@pytest.fixture
def ambulancia_test():
    return Ambulancia.objects.create(
        placa='DAO-TEST',
        estado='Disponible',
        tipo_A='Tipo I',
        marca='Test',
        fecha_adquisicion='2024-01-01'
    )

@pytest.mark.django_db
def test_dao_create_ambulancia_valida():
    # Precondición: DB vacía
    assert Ambulancia.objects.count() == 0
    
    # Pasos: Usar DAO para crear
    ambulancia = AmbulanciaDAO.crear(placa='XYZ-789', estado='Disponible', tipo='Tipo I', marca='Toyota', fecha_adquisicion=timezone.now(), capacidad=6)
    
    # Resultado esperado
    assert Ambulancia.objects.count() == 1
    assert ambulancia.placa == 'XYZ-789'

@pytest.mark.django_db
def test_dao_obtener_todas_ambulancias(ambulancia_test):
    """Test obtener todas las ambulancias"""
    ambulancias = AmbulanciaDAO.obtener_todas()
    assert ambulancia_test in ambulancias
    assert ambulancias.count() >= 1

@pytest.mark.django_db
def test_dao_filtrar_ambulancias_por_estado(ambulancia_test):
    """Test filtrar por estado"""
    ambulancias = AmbulanciaDAO.filtrar_ambulancias(estado='Disponible')
    assert ambulancia_test in ambulancias

@pytest.mark.django_db
def test_dao_filtrar_ambulancias_por_placa(ambulancia_test):
    """Test filtrar por placa"""
    ambulancias = AmbulanciaDAO.filtrar_ambulancias(placa='DAO')
    assert ambulancia_test in ambulancias

@pytest.mark.django_db
def test_dao_obtener_por_id(ambulancia_test):
    """Test obtener ambulancia por ID"""
    ambulancia = AmbulanciaDAO.obtener_por_id(ambulancia_test.id)
    assert ambulancia.placa == 'DAO-TEST'

@pytest.mark.django_db
def test_dao_actualizar_ambulancia(ambulancia_test):
    """Test actualizar ambulancia"""
    datos = {'estado': 'En Servicio', 'marca': 'Ford'}
    ambulancia = AmbulanciaDAO.actualizar(ambulancia_test, datos)
    assert ambulancia.estado == 'En Servicio'
    assert ambulancia.marca == 'Ford'

@pytest.mark.django_db
def test_dao_averia_listar_todas(ambulancia_test):
    """Test listar todas las averías"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_test,
        nombre_colaborador='Test'
    )
    averias = AveriaDAO.listar_todas()
    assert averias.count() >= 1

@pytest.mark.django_db
def test_dao_averia_buscar_por_placa(ambulancia_test):
    """Test buscar averías por placa"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_test,
        nombre_colaborador='Test'
    )
    averias = AveriaDAO.buscar_por_placa('DAO-TEST')
    assert averias.count() >= 1

@pytest.mark.django_db
def test_dao_averia_filtrar_por_fecha(ambulancia_test):
    """Test filtrar averías por fecha"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_test,
        nombre_colaborador='Test'
    )
    averias = AveriaDAO.filtrar_por_fecha(date.today())
    assert averias.count() >= 1

@pytest.mark.django_db
def test_dao_combustible_obtener_todos(ambulancia_test):
    """Test obtener todos los registros de combustible"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_test
    )
    registros = CombustibleDAO.obtener_todos()
    assert registros.count() >= 1

@pytest.mark.django_db
def test_dao_combustible_buscar_por_placa(ambulancia_test):
    """Test buscar combustible por placa"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_test
    )
    registros = CombustibleDAO.buscar_por_placa('DAO-TEST')
    assert registros.count() >= 1

@pytest.mark.django_db
def test_dao_combustible_filtrar_por_fecha(ambulancia_test):
    """Test filtrar combustible por fecha"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_test
    )
    registros = CombustibleDAO.filtrar_por_fecha(date.today())
    assert registros.count() >= 1