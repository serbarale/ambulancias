# ambulancias/tests/test_services.py
import pytest
from ambulancias.services.ambulancia_service import AmbulanciaService
from ambulancias.services.averia_service import AveriaService
from ambulancias.services.combustible_service import CombustibleService
from ambulancias.models import Ambulancia, Avería, Combustible
from datetime import date

@pytest.fixture
def ambulancia_service_test():
    return Ambulancia.objects.create(
        placa='SVC-001',
        estado='Disponible',
        tipo_A='Tipo I',
        marca='Toyota',
        fecha_adquisicion='2024-01-01'
    )

@pytest.mark.django_db
def test_service_listar_filtradas_sin_filtros(ambulancia_service_test):
    """Test listar ambulancias sin filtros"""
    ambulancias = AmbulanciaService.listar_filtradas(None, None, None)
    assert ambulancia_service_test in ambulancias

@pytest.mark.django_db
def test_service_listar_filtradas_con_estado(ambulancia_service_test):
    """Test listar ambulancias filtrando por estado"""
    ambulancias = AmbulanciaService.listar_filtradas('Disponible', None, None)
    assert ambulancia_service_test in ambulancias

@pytest.mark.django_db
def test_service_listar_filtradas_con_placa(ambulancia_service_test):
    """Test listar ambulancias filtrando por placa"""
    ambulancias = AmbulanciaService.listar_filtradas(None, None, 'SVC')
    assert ambulancia_service_test in ambulancias

@pytest.mark.django_db
def test_service_obtener_ambulancia(ambulancia_service_test):
    """Test obtener ambulancia por ID"""
    ambulancia = AmbulanciaService.obtener_ambulancia(ambulancia_service_test.id)
    assert ambulancia.placa == 'SVC-001'

@pytest.mark.django_db
def test_service_actualizar_ambulancia(ambulancia_service_test):
    """Test actualizar ambulancia"""
    datos = {'estado': 'En Servicio'}
    AmbulanciaService.actualizar_ambulancia(ambulancia_service_test.id, datos)
    ambulancia_service_test.refresh_from_db()
    assert ambulancia_service_test.estado == 'En Servicio'

@pytest.mark.django_db
def test_service_averia_registrar_valida(ambulancia_service_test):
    """Test registrar avería válida"""
    datos = {
        'tipoF': 'Motor',
        'descripcion_averia': 'Falla en motor',
        'ambulancia': str(ambulancia_service_test.id),
        'nombre_colaborador': 'Juan Perez'
    }
    averia = AveriaService.registrar_averia(datos)
    assert averia.tipoF == 'Motor'
    assert Avería.objects.count() == 1

@pytest.mark.django_db
def test_service_averia_sin_tipo_falla():
    """Test registrar avería sin tipo de falla"""
    datos = {
        'descripcion_averia': 'Falla',
        'ambulancia': '1',
        'nombre_colaborador': 'Juan'
    }
    with pytest.raises(ValueError, match="Faltan campos obligatorios"):
        AveriaService.registrar_averia(datos)

@pytest.mark.django_db
def test_service_averia_ambulancia_no_existe():
    """Test registrar avería con ambulancia inexistente"""
    datos = {
        'tipoF': 'Motor',
        'descripcion_averia': 'Falla',
        'ambulancia': '99999',
        'nombre_colaborador': 'Juan'
    }
    with pytest.raises(ValueError, match="Ambulancia no encontrada"):
        AveriaService.registrar_averia(datos)

@pytest.mark.django_db
def test_service_averia_obtener_todas(ambulancia_service_test):
    """Test obtener todas las averías"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_service_test,
        nombre_colaborador='Test'
    )
    averias = AveriaService.obtener_todas()
    assert averias.count() >= 1

@pytest.mark.django_db
def test_service_averia_buscar_por_placa(ambulancia_service_test):
    """Test buscar averías por placa"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_service_test,
        nombre_colaborador='Test'
    )
    averias = AveriaService.buscar_por_placa('SVC-001')
    assert averias.count() >= 1

@pytest.mark.django_db
def test_service_averia_filtrar_por_fecha(ambulancia_service_test):
    """Test filtrar averías por fecha"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_service_test,
        nombre_colaborador='Test'
    )
    averias = AveriaService.filtrar_por_fecha(date.today())
    assert averias.count() >= 1

@pytest.mark.django_db
def test_service_combustible_registrar_valido(ambulancia_service_test):
    """Test registrar combustible válido"""
    datos = {
        'fecha_combustible': '2024-11-22',
        'comb_inicial': '50.0',
        'comb_final': '30.0',
        'km_inicial': '1000',
        'km_final': '1100',
        'nombre_colaborador': 'Juan Perez',
        'ambulancia_id': ambulancia_service_test.id
    }
    combustible = CombustibleService.registrar_combustible(datos)
    assert combustible.comb_inicial == 50.0
    assert Combustible.objects.count() == 1

@pytest.mark.django_db
def test_service_combustible_obtener_todos(ambulancia_service_test):
    """Test obtener todos los registros de combustible"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_service_test
    )
    registros = CombustibleService.obtener_todos()
    assert registros.count() >= 1

@pytest.mark.django_db
def test_service_combustible_buscar_por_placa(ambulancia_service_test):
    """Test buscar combustible por placa"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_service_test
    )
    registros = CombustibleService.buscar_por_placa('SVC-001')
    assert registros.count() >= 1

@pytest.mark.django_db
def test_service_combustible_filtrar_por_fecha(ambulancia_service_test):
    """Test filtrar combustible por fecha"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_service_test
    )
    registros = CombustibleService.filtrar_por_fecha(date.today())
    assert registros.count() >= 1
