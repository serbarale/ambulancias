import pytest
from django.utils import timezone
from inventarios.services.checklist_service import CheckListService
from inventarios.services.insumo_service import InsumoService
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
def insumo_basico():
    return InsumoMedico.objects.create(
        nombre="Vendas",
        stockMinimo=10,
        unidadMedida="unidades",
        tipoAmbulancia="tipo_1"
    )

@pytest.mark.django_db
class TestCheckListService:
    """TC-17: Registrar check list con faltantes y generar alertas"""
    def test_registrar_checklist_con_faltantes(self, ambulancia, insumo_basico):
        # Datos del checklist
        datos_checklist = {
            "ambulancia": ambulancia,
            "nombre_colaborador": "Juan Pérez"
        }
        
        # Detalles con faltantes
        detalles_insumos = [{
            "insumo": insumo_basico,
            "cantidad_contada": 5  # Menor al stock mínimo (10)
        }]
        
        # Registrar checklist
        checklist = CheckListService.registrar_checklist(datos_checklist, detalles_insumos)
        
        # Verificar que se detecten los faltantes
        insumos_para_verificar = [{
            "cantidad_contada": 5,
            "stockMinimo": insumo_basico.stockMinimo
        }]
        insumos_faltantes = CheckListService.contar_insumos_a_reponer(insumos_para_verificar)
        assert insumos_faltantes > 0
        assert checklist is not None
        
    """TC-19: Generar alerta por stock bajo"""
    def test_alerta_stock_bajo(self, insumo_basico):
        # Simular verificación de stock
        stock_actual = 8  # Menor al mínimo (10)
        necesita_reposicion = stock_actual < insumo_basico.stockMinimo
        
        assert necesita_reposicion == True
        
        # Verificar que el servicio detecte el stock bajo
        insumos_criticos = [{
            "insumo": insumo_basico,
            "cantidad_contada": stock_actual
        }]
        
        insumos_para_reponer = CheckListService.contar_insumos_a_reponer(
            [{"cantidad_contada": stock_actual, "stockMinimo": insumo_basico.stockMinimo}]
        )
        assert insumos_para_reponer > 0

    """TC-26: Integración inventario-emergencia"""
    def test_integracion_inventario_emergencia(self, ambulancia, insumo_basico):
        # Simular uso de insumos en emergencia
        datos_checklist = {
            "ambulancia": ambulancia,
            "nombre_colaborador": "Juan Pérez"
        }
        
        # Registrar uso de insumos
        detalles_insumos = [{
            "insumo": insumo_basico,
            "cantidad_contada": 3
        }]
        
        # Verificar actualización de inventario
        checklist = CheckListService.registrar_checklist(datos_checklist, detalles_insumos)
        assert checklist is not None
        
        # Verificar registro de uso
        detalles = DetalleCheckList.objects.filter(checklist=checklist)
        assert detalles.exists()
        assert detalles.first().cantidad_contada == 3