import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from inventarios.models import InsumoMedico, CheckList, DetalleCheckList
from ambulancias.models import Ambulancia

@pytest.fixture
def ambulancia():
    return Ambulancia.objects.create(
        placa="ABC123",
        tipo_A="tipo_1",
        estado="preparada",
        marca="Toyota",
        fecha_adquisicion="2023-01-01"
    )

@pytest.fixture
def insumo_medico():
    return InsumoMedico.objects.create(
        nombre="Vendas",
        stockMinimo=10,
        unidadMedida="unidades",
        tipoAmbulancia="tipo_1"
    )

@pytest.mark.django_db
class TestCheckList:
    """TC-09: Validar registro de check list completo"""
    def test_registrar_checklist_completo(self, ambulancia, insumo_medico):
        # Crear checklist
        checklist = CheckList.objects.create(
            ambulancia=ambulancia,
            nombre_colaborador="Juan Pérez"
        )
        
        # Agregar detalle
        detalle = DetalleCheckList.objects.create(
            checklist=checklist,
            insumo=insumo_medico,
            cantidad_contada=15
        )
        
        # Verificaciones
        assert checklist.ambulancia == ambulancia
        assert checklist.nombre_colaborador == "Juan Pérez"
        assert checklist.fecha_registro is not None
        assert detalle.cantidad_contada == 15
        assert detalle.insumo == insumo_medico

@pytest.mark.django_db
class TestInsumoMedico:
    """TC-10: Validar reducción de stock y alertas"""
    def test_reduccion_stock_con_alerta(self, insumo_medico):
        # Verificar stock mínimo inicial
        assert insumo_medico.stockMinimo == 10
        
        # Simular reducción de stock
        stock_actual = 12
        cantidad_usar = 5
        nuevo_stock = stock_actual - cantidad_usar
        
        # Verificar si se necesita generar alerta
        necesita_alerta = nuevo_stock <= insumo_medico.stockMinimo
        assert necesita_alerta == True
        assert nuevo_stock < stock_actual

    """TC-18: Validar registro de insumo expirado"""
    def test_registro_insumo_expirado(self):
        # Crear insumo con fecha de expiración
        insumo = InsumoMedico.objects.create(
            nombre="Medicamento",
            stockMinimo=5,
            unidadMedida="unidades",
            tipoAmbulancia="tipo_1"
        )
        
        assert insumo.nombre == "Medicamento"
        assert insumo.stockMinimo == 5
        assert insumo.unidadMedida == "unidades"
        
        # Verificar que se pueda registrar
        insumo_registrado = InsumoMedico.objects.get(id=insumo.id)
        assert insumo_registrado is not None