"""TC-11: Pruebas para la creación de solicitudes de reposición"""
import pytest
from django.utils import timezone
from datetime import datetime, timedelta
from inventarios.models import InsumoMedico, SolicitudReposicion
from inventarios.services.insumo_service import InsumoService

@pytest.mark.django_db
class TestSolicitudReposicion:
    def test_crear_solicitud_reposicion(self):
        # Crear insumo con stock bajo
        insumo = InsumoMedico.objects.create(
            nombre="Guantes",
            stockMinimo=100,
            stock_actual=50,
            unidadMedida="pares",
            tipoAmbulancia="tipo_1"
        )
        
        # Crear solicitud de reposición
        solicitud = SolicitudReposicion.objects.create(
            insumo=insumo,
            cantidad_solicitada=100,
            observaciones="Reposición urgente"
        )
        
        # Verificaciones
        assert solicitud.insumo == insumo
        assert solicitud.cantidad_solicitada == 100
        assert solicitud.estado == "pendiente"
        assert solicitud.fecha_solicitud is not None
        
    def test_alerta_stock_bajo_automatica(self):
        # Crear insumo con stock crítico
        insumo = InsumoMedico.objects.create(
            nombre="Vendas",
            stockMinimo=50,
            stock_actual=10,
            unidadMedida="unidades",
            tipoAmbulancia="tipo_1"
        )
        
        # Verificar si se necesita reposición
        necesita_reposicion = insumo.stock_actual < insumo.stockMinimo
        assert necesita_reposicion == True
        
        # Crear solicitud automática
        solicitud = SolicitudReposicion.objects.create(
            insumo=insumo,
            cantidad_solicitada=insumo.stockMinimo - insumo.stock_actual,
            observaciones="Reposición automática por stock bajo"
        )
        
        assert solicitud.cantidad_solicitada == 40  # 50 - 10
        assert "automática" in solicitud.observaciones.lower()

    def test_insumo_expirado_con_reposicion(self):
        # Crear insumo próximo a expirar
        fecha_expiracion = timezone.now().date() + timedelta(days=5)
        insumo = InsumoMedico.objects.create(
            nombre="Medicamento",
            stockMinimo=20,
            stock_actual=30,
            fecha_expiracion=fecha_expiracion,
            unidadMedida="unidades",
            tipoAmbulancia="tipo_1"
        )
        
        # Verificar proximidad a expiración
        dias_para_expirar = (insumo.fecha_expiracion - timezone.now().date()).days
        necesita_reposicion = dias_para_expirar <= 7
        assert necesita_reposicion == True
        
        # Crear solicitud de reposición
        solicitud = SolicitudReposicion.objects.create(
            insumo=insumo,
            cantidad_solicitada=insumo.stockMinimo,
            observaciones=f"Reposición por proximidad a fecha de expiración ({dias_para_expirar} días)"
        )
        
        assert solicitud is not None
        assert "expiración" in solicitud.observaciones.lower()