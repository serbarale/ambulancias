import pytest
from django.urls import reverse
from django.test import Client
from ambulancias.models import Ambulancia, Avería, Combustible
from datetime import date

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def ambulancia_existente():
    return Ambulancia.objects.create(
        placa='ABC-123',
        estado='Disponible',
        tipo_A='Tipo I',
        marca='Toyota',
        fecha_adquisicion='2024-01-01'
    )

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

@pytest.mark.django_db
def test_registrar_ambulancia_get(client):
    """Test GET del formulario de registro"""
    url = reverse('ambulancias:registrar_ambulancia')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'estados' in response.context
    assert 'tipos' in response.context

@pytest.mark.django_db
def test_listar_ambulancias(client, ambulancia_existente):
    """Test listar todas las ambulancias"""
    url = reverse('ambulancias:listar_ambulancias')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'ambulancias' in response.context
    assert ambulancia_existente in response.context['ambulancias']

@pytest.mark.django_db
def test_listar_ambulancias_filtro_estado(client, ambulancia_existente):
    """Test listar ambulancias con filtro de estado"""
    url = reverse('ambulancias:listar_ambulancias') + '?estado=Disponible'
    response = client.get(url)
    
    assert response.status_code == 200
    assert ambulancia_existente in response.context['ambulancias']

@pytest.mark.django_db
def test_listar_ambulancias_filtro_placa(client, ambulancia_existente):
    """Test listar ambulancias con filtro de placa"""
    url = reverse('ambulancias:listar_ambulancias') + '?placa=ABC'
    response = client.get(url)
    
    assert response.status_code == 200
    assert ambulancia_existente in response.context['ambulancias']

@pytest.mark.django_db
def test_editar_ambulancia_get(client, ambulancia_existente):
    """Test GET del formulario de edición"""
    url = reverse('ambulancias:editar_ambulancia', kwargs={'id': ambulancia_existente.id})
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'ambulancia' in response.context
    assert response.context['ambulancia'].placa == 'ABC-123'

@pytest.mark.django_db
def test_editar_ambulancia_post(client, ambulancia_existente):
    """Test POST para editar ambulancia"""
    url = reverse('ambulancias:editar_ambulancia', kwargs={'id': ambulancia_existente.id})
    data = {
        'placa': 'ABC-123',
        'estado': 'En Reparación',
        'tipo_A': 'Tipo II',
        'marca': 'Ford',
        'fecha_adquisicion': '2024-01-01'
    }
    response = client.post(url, data)
    
    assert response.status_code == 302
    ambulancia_existente.refresh_from_db()
    assert ambulancia_existente.estado == 'En Reparación'
    assert ambulancia_existente.tipo_A == 'Tipo II'

@pytest.mark.django_db
def test_submenu_ambulancias(client):
    """Test vista de submenu"""
    url = reverse('ambulancias:submenu_ambulancias')
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_registrar_averia_get(client, ambulancia_existente):
    """Test GET formulario de registro de avería"""
    url = reverse('ambulancias:registrar_averia')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'ambulancias' in response.context

@pytest.mark.django_db
def test_registrar_averia_post(client, ambulancia_existente):
    """Test POST para registrar avería"""
    url = reverse('ambulancias:registrar_averia')
    data = {
        'tipoF': 'Motor',
        'descripcion_averia': 'Falla en motor',
        'ambulancia': ambulancia_existente.id,
        'nombre_colaborador': 'Juan Perez'
    }
    response = client.post(url, data)
    
    assert response.status_code == 302
    assert Avería.objects.count() == 1

@pytest.mark.django_db
def test_lista_averias(client, ambulancia_existente):
    """Test listar averías"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_existente,
        nombre_colaborador='Test'
    )
    url = reverse('ambulancias:lista_averias')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'averias' in response.context

@pytest.mark.django_db
def test_lista_averias_filtro_placa(client, ambulancia_existente):
    """Test listar averías con filtro de placa"""
    Avería.objects.create(
        tipoF='Motor',
        descripcion_averia='Test',
        ambulancia=ambulancia_existente,
        nombre_colaborador='Test'
    )
    url = reverse('ambulancias:lista_averias') + f'?placa={ambulancia_existente.placa}'
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_registrar_combustible_get(client, ambulancia_existente):
    """Test GET formulario de registro de combustible"""
    url = reverse('ambulancias:registrar_combustible')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'ambulancias' in response.context

@pytest.mark.django_db
def test_registrar_combustible_post(client, ambulancia_existente):
    """Test POST para registrar combustible"""
    url = reverse('ambulancias:registrar_combustible')
    data = {
        'fecha_combustible': '2024-11-22',
        'comb_inicial': '50.0',
        'comb_final': '30.0',
        'km_inicial': '1000',
        'km_final': '1100',
        'nombre_colaborador': 'Juan Perez',
        'ambulancia': ambulancia_existente.id
    }
    response = client.post(url, data)
    
    assert response.status_code == 302
    assert Combustible.objects.count() == 1

@pytest.mark.django_db
def test_lista_combustible(client, ambulancia_existente):
    """Test listar registros de combustible"""
    Combustible.objects.create(
        fecha_combustible=date.today(),
        comb_inicial=50.0,
        comb_final=30.0,
        km_inicial=1000,
        km_final=1100,
        nombre_colaborador='Test',
        ambulancia=ambulancia_existente
    )
    url = reverse('ambulancias:lista_combustible')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'registros' in response.context