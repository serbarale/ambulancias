import pytest
from django.urls import reverse
from inventarios.models import Insumo, CheckList
from ambulancias.models import Ambulancia

pytestmark = pytest.mark.django_db

@pytest.fixture
def ambulancia_inventario():
    return Ambulancia.objects.create(
        placa='INV-001',
        estado='Disponible',
        tipo_A='Tipo I',
        marca='Toyota',
        fecha_adquisicion='2024-01-01'
    )

@pytest.fixture
def insumo_test():
    return Insumo.objects.create(
        nombre='Vendas',
        cantidad=100,
        tipo_ambulancia='Tipo I',
        unidad_medida='und'
    )

def test_submenu_inventarios(client):
    """Test vista de submenu inventarios"""
    url = reverse('inventarios:submenu_inventarios')
    response = client.get(url)
    assert response.status_code == 200

def test_buscar_ambulancia_checklist_sin_filtro(client, ambulancia_inventario):
    """Test buscar ambulancia sin filtro"""
    url = reverse('inventarios:buscar_ambulancia_checklist')
    response = client.get(url)
    assert response.status_code == 200
    assert 'ambulancias' in response.context
    assert ambulancia_inventario in response.context['ambulancias']

def test_buscar_ambulancia_checklist_con_placa(client, ambulancia_inventario):
    """Test buscar ambulancia por placa"""
    url = reverse('inventarios:buscar_ambulancia_checklist') + '?placa=INV'
    response = client.get(url)
    assert response.status_code == 200
    assert ambulancia_inventario in response.context['ambulancias']

def test_historial_checklist(client, ambulancia_inventario):
    """Test ver historial de checklist"""
    url = reverse('inventarios:historial_checklist', kwargs={'ambulancia_id': ambulancia_inventario.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'checklists' in response.context
    assert 'ambulancia' in response.context

def test_registrar_checklist_get(client, ambulancia_inventario, insumo_test):
    """Test GET formulario de registro de checklist"""
    url = reverse('inventarios:registrar_checklist', kwargs={'ambulancia_id': ambulancia_inventario.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'ambulancia' in response.context
    assert 'insumos' in response.context

def test_registrar_checklist_post(client, ambulancia_inventario, insumo_test):
    """Test POST para registrar checklist"""
    url = reverse('inventarios:registrar_checklist', kwargs={'ambulancia_id': ambulancia_inventario.id})
    data = {
        'nombre_colaborador': 'Juan Perez',
        f'insumo_{insumo_test.id}': '10'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert CheckList.objects.count() >= 1

def test_listar_insumos(client, insumo_test):
    """Test listar insumos"""
    url = reverse('inventarios:listar_insumos')
    response = client.get(url)
    assert response.status_code == 200
    assert 'insumos' in response.context
    assert insumo_test in response.context['insumos']

def test_listar_insumos_con_filtro(client, insumo_test):
    """Test listar insumos con filtro de nombre"""
    url = reverse('inventarios:listar_insumos') + '?nombre=Vendas'
    response = client.get(url)
    assert response.status_code == 200
    assert insumo_test in response.context['insumos']

def test_crear_insumo_get(client):
    """Test GET formulario de crear insumo"""
    url = reverse('inventarios:crear_insumo')
    response = client.get(url)
    assert response.status_code == 200

def test_crear_insumo_post(client):
    """Test POST para crear insumo"""
    url = reverse('inventarios:crear_insumo')
    data = {
        'nombre': 'Guantes',
        'cantidad': 200,
        'tipo_ambulancia': 'Tipo I',
        'unidad_medida': 'par'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Insumo.objects.filter(nombre='Guantes').exists()

def test_actualizar_insumo_get(client, insumo_test):
    """Test GET formulario de actualizar insumo"""
    url = reverse('inventarios:actualizar_insumo', kwargs={'id': insumo_test.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'insumo' in response.context

def test_actualizar_insumo_post(client, insumo_test):
    """Test POST para actualizar insumo"""
    url = reverse('inventarios:actualizar_insumo', kwargs={'id': insumo_test.id})
    data = {
        'nombre': 'Vendas',
        'cantidad': 150,
        'tipo_ambulancia': 'Tipo I',
        'unidad_medida': 'und'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    insumo_test.refresh_from_db()
    assert insumo_test.cantidad == 150

def test_alertas_stock_critico(client):
    """Test ver alertas de stock crítico"""
    Insumo.objects.create(
        nombre='Insumo Crítico',
        cantidad=5,
        tipo_ambulancia='Tipo I',
        unidad_medida='und'
    )
    url = reverse('inventarios:alertas_stock_critico')
    response = client.get(url)
    assert response.status_code == 200
    assert 'insumos_criticos' in response.context
