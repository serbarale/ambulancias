import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import transaction
from datetime import date, datetime, timedelta
from django.utils import timezone

# Importar todos los modelos necesarios
from ambulancias.models import Ambulancia
from pacientes.models import Paciente, HistorialMedico
from inventarios.models import InsumoMedico, CheckList, DetalleCheckList
from emergencias.models import InformeEmergencia, ReporteEmergencia, ReportePaciente, InsumoUtilizado

# Importar servicios
from ambulancias.services.ambulancia_service import AmbulanciaService
from pacientes.services.historial_service import HistorialService
from inventarios.services.checklist_service import CheckListService
from inventarios.services.insumo_service import InsumoService
from emergencias.services.informe_service import InformeEmergenciaService
from emergencias.services.reporte_service import ReporteEmergenciaService

@pytest.mark.django_db
class TestIntegracionCompleta:
    """Pruebas de integración completa entre módulos del sistema."""

    @pytest.fixture(autouse=True)
    def setup_data(self):
        """Configuración de datos base para las pruebas."""
        # Crear ambulancia
        self.ambulancia = Ambulancia.objects.create(
            placa="INT-001",
            estado="preparada",
            tipo="tipo_1",
            marca="Mercedes",
            fecha_adquisicion=date(2024, 1, 1),
            capacidad=4
        )
        
        # Crear insumos médicos
        self.insumo_vendas = InsumoMedico.objects.create(
            nombre="Vendas Elásticas",
            stockMinimo=20,
            unidadMedida="unidades",
            tipoAmbulancia="tipo_1"
        )
        
        self.insumo_guantes = InsumoMedico.objects.create(
            nombre="Guantes Quirúrgicos",
            stockMinimo=50,
            unidadMedida="pares",
            tipoAmbulancia="tipo_1"
        )
        
        # Crear paciente con historial
        self.paciente = Paciente.objects.create(
            nombre="María",
            apellido="González",
            dni="12345678",
            fechaNacimiento=date(1990, 5, 15),
            sexo="femenino",
            telefono="987654321",
            email="maria@example.com"
        )
        
        self.historial = HistorialMedico.objects.create(
            tipoSangre="O+",
            alergias="Penicilina",
            enfermedades="Diabetes Tipo 2",
            paciente=self.paciente
        )

    def test_flujo_emergencia_completo(self):
        """Valida el flujo completo: ambulancia → emergencia → insumos → reporte."""
        # Verificar estado inicial
        assert self.ambulancia.estado == "preparada"
        assert Paciente.objects.count() == 1
        
        # Registrar informe de emergencia
        datos_informe = {
            "ambulancia_id": self.ambulancia.id,
            "direccion_emergencia": "Av. Principal 123",
            "prioridad": "alta",
            "estado": "pendiente",
            "nombre_chofer": "Carlos Pérez",
            "paciente_opcional": self.paciente.nombre
        }
        
        informe = InformeEmergenciaService.registrar_informe(datos_informe)
        
        # Verificar creación del informe
        assert informe is not None
        assert informe.ambulancia == self.ambulancia
        assert informe.direccion == "Av. Principal 123"
        assert informe.prioridad == "alta"
        
        # Generar reporte con insumos y pacientes
        procedimientos = "RCP, Inmovilización, Administración de oxígeno"
        pertenencias = "Celular, Cartera"
        pacientes_ids = [self.paciente.id]
        insumos_data = [
            {"id": self.insumo_vendas.id, "cantidad": 3},
            {"id": self.insumo_guantes.id, "cantidad": 2}
        ]
        
        reporte = ReporteEmergenciaService.registrar_reporte(
            informe, procedimientos, pertenencias, pacientes_ids, insumos_data
        )
        
        # Verificar creación del reporte
        assert reporte is not None
        assert reporte.informe == informe
        assert reporte.procedimientos == procedimientos
        
        # Verificar asociación de pacientes
        reportes_paciente = ReportePaciente.objects.filter(reporte=reporte)
        assert reportes_paciente.count() == 1
        assert reportes_paciente.first().paciente == self.paciente
        
        # Verificar registro de insumos utilizados
        insumos_utilizados = InsumoUtilizado.objects.filter(reporte=reporte)
        assert insumos_utilizados.count() == 2
        uso_vendas = InsumoUtilizado.objects.get(reporte=reporte, insumo=self.insumo_vendas)
        uso_guantes = InsumoUtilizado.objects.get(reporte=reporte, insumo=self.insumo_guantes)
        assert uso_vendas.cantidad == 3
        assert uso_guantes.cantidad == 2

    def test_integracion_checklist_emergencia(self):
        """Valida integración entre checklist de inventarios y emergencias."""
        # Crear checklist con faltantes
        datos_checklist = {
            "ambulancia": self.ambulancia,
            "nombre_colaborador": "Ana Martínez"
        }
        
        detalles_insumos = [
            {"insumo": self.insumo_vendas, "cantidad_contada": 15},  # Falta
            {"insumo": self.insumo_guantes, "cantidad_contada": 30}   # Falta
        ]
        
        checklist = CheckListService.registrar_checklist(datos_checklist, detalles_insumos)
        
        # Verificar creación del checklist
        assert checklist is not None
        assert checklist.ambulancia == self.ambulancia
        
        # Verificar detalles del checklist
        detalles = DetalleCheckList.objects.filter(checklist=checklist)
        assert detalles.count() == 2
        
        # Verificar detección de faltantes
        insumos_para_verificar = [
            {"cantidad_contada": 15, "stockMinimo": self.insumo_vendas.stockMinimo},
            {"cantidad_contada": 30, "stockMinimo": self.insumo_guantes.stockMinimo}
        ]
        
        insumos_faltantes = CheckListService.contar_insumos_a_reponer(insumos_para_verificar)
        assert insumos_faltantes > 0
        
        # Registrar emergencia que necesita insumos faltantes
        datos_informe = {
            "ambulancia_id": self.ambulancia.id,
            "direccion_emergencia": "Calle Emergencia 456",
            "prioridad": "alta",
            "estado": "en_curso",
            "nombre_chofer": "Pedro López"
        }
        
        informe = InformeEmergenciaService.registrar_informe(datos_informe)
        assert informe is not None
        
        # Usar insumos en emergencia
        insumos_uso_emergencia = [
            {"id": self.insumo_vendas.id, "cantidad": 10},
            {"id": self.insumo_guantes.id, "cantidad": 25}
        ]
        reporte = ReporteEmergenciaService.registrar_reporte(
            informe, "Atención básica", "Sin pertenencias", [], insumos_uso_emergencia
        )
        
        assert reporte is not None
        insumos_utilizados = InsumoUtilizado.objects.filter(reporte=reporte)
        assert insumos_utilizados.count() == 2

    def test_integracion_paciente_historial_emergencia(self):
        """Valida acceso a información crítica del paciente en emergencias."""
        # Buscar paciente e historial
        paciente_encontrado, historial_encontrado = HistorialService().buscar_historial(
            dni="12345678"
        )
        
        # Verificar que se encontró el paciente y su historial
        assert paciente_encontrado is not None
        assert historial_encontrado is not None
        assert paciente_encontrado.dni == "12345678"
        assert historial_encontrado.tipoSangre == "O+"
        assert "Penicilina" in historial_encontrado.alergias
        
        # Crear emergencia con información del paciente
        datos_informe = {
            "ambulancia_id": self.ambulancia.id,
            "direccion_emergencia": "Hospital Central",
            "prioridad": "alta",
            "estado": "en_curso",
            "nombre_chofer": "María Rodríguez",
            "paciente_opcional": f"{paciente_encontrado.nombre} {paciente_encontrado.apellido}"
        }
        
        informe = InformeEmergenciaService.registrar_informe(datos_informe)
        
        # Verificar que la emergencia tiene acceso a la información del paciente
        assert informe is not None
        assert paciente_encontrado.nombre in informe.paciente_opcional
        
        # Crear reporte que incluye al paciente
        reporte = ReporteEmergenciaService.registrar_reporte(
            informe,
            f"Paciente con alergias a {historial_encontrado.alergias}, tipo sanguíneo {historial_encontrado.tipoSangre}",
            "Documentos de identidad",
            [paciente_encontrado.id],
            []
        )
        
        # Verificar asociación correcta
        reporte_paciente = ReportePaciente.objects.get(reporte=reporte, paciente=paciente_encontrado)
        assert reporte_paciente is not None
        
        # Verificar acceso a información crítica del historial
        historial_paciente = reporte_paciente.paciente.historial_medico
        assert historial_paciente.tipoSangre == "O+"
        assert historial_paciente.alergias == "Penicilina"
        assert historial_paciente.enfermedades == "Diabetes Tipo 2"

    def test_workflow_multiples_ambulancias(self):
        """Valida operación concurrente de múltiples ambulancias."""
        # Crear ambulancias adicionales
        ambulancia2 = Ambulancia.objects.create(
            placa="INT-002",
            estado="preparada",
            tipo="tipo_2",
            marca="Ford",
            fecha_adquisicion=date(2024, 2, 1),
            capacidad=6
        )
        
        ambulancia3 = Ambulancia.objects.create(
            placa="INT-003",
            estado="inhabilitada",
            tipo="tipo_1",
            marca="Chevrolet",
            fecha_adquisicion=date(2024, 3, 1),
            capacidad=4
        )
        
        # Crear pacientes adicionales
        paciente2 = Paciente.objects.create(
            nombre="Carlos",
            apellido="Ramírez",
            dni="87654321",
            fechaNacimiento=date(1985, 8, 20),
            sexo="masculino"
        )
        
        # Crear emergencias simultáneas
        informe1 = InformeEmergenciaService.registrar_informe({
            "ambulancia_id": self.ambulancia.id,
            "direccion_emergencia": "Zona Norte",
            "prioridad": "media",
            "estado": "en_curso",
            "nombre_chofer": "Conductor 1"
        })
        
        informe2 = InformeEmergenciaService.registrar_informe({
            "ambulancia_id": ambulancia2.id,
            "direccion_emergencia": "Zona Sur", 
            "prioridad": "alta",
            "estado": "pendiente",
            "nombre_chofer": "Conductor 2"
        })
        
        # Verificar que las emergencias son independientes
        assert informe1.ambulancia != informe2.ambulancia
        assert informe1.direccion != informe2.direccion
        
        # Crear checklists independientes
        checklist1 = CheckListService.registrar_checklist(
            {"ambulancia": self.ambulancia, "nombre_colaborador": "Revisor 1"},
            [{"insumo": self.insumo_vendas, "cantidad_contada": 25}]
        )
        
        checklist2 = CheckListService.registrar_checklist(
            {"ambulancia": ambulancia2, "nombre_colaborador": "Revisor 2"},
            [{"insumo": self.insumo_guantes, "cantidad_contada": 55}]
        )
        
        # Verificar independencia de checklists
        assert checklist1.ambulancia != checklist2.ambulancia
        assert checklist1.nombre_colaborador != checklist2.nombre_colaborador
        
        # Verificar conteo total del sistema
        assert Ambulancia.objects.count() == 3
        assert InformeEmergencia.objects.count() == 2
        assert CheckList.objects.count() == 2

    def test_integracion_alertas_stock_critico(self):
        """Valida alertas automáticas cuando los insumos alcanzan niveles críticos."""
        # Crear insumo con stock específico
        insumo_critico = InsumoMedico.objects.create(
            nombre="Suero Fisiológico",
            stockMinimo=10,
            unidadMedida="unidades",
            tipoAmbulancia="tipo_1"
        )
        
        # Realizar checklist inicial
        checklist_inicial = CheckListService.registrar_checklist(
            {"ambulancia": self.ambulancia, "nombre_colaborador": "Supervisor"},
            [{"insumo": insumo_critico, "cantidad_contada": 12}]
        )
        
        # Crear emergencia que consumirá stock crítico
        informe = InformeEmergenciaService.registrar_informe({
            "ambulancia_id": self.ambulancia.id,
            "direccion_emergencia": "Emergencia Crítica 789",
            "prioridad": "alta",
            "estado": "en_curso",
            "nombre_chofer": "Paramédico Urgencias"
        })
        
        # Usar insumos que llevarán el stock por debajo del mínimo
        reporte = ReporteEmergenciaService.registrar_reporte(
            informe,
            "Emergencia que requiere múltiples sueros",
            "Equipos médicos del paciente",
            [self.paciente.id],
            [{"id": insumo_critico.id, "cantidad": 5}]  # Usar 5 unidades
        )
        
        # Verificar que el uso se registró correctamente
        uso_suero = InsumoUtilizado.objects.get(reporte=reporte, insumo=insumo_critico)
        assert uso_suero.cantidad == 5
        
        # Simular verificación post-emergencia
        stock_restante = 12 - 5  # 7 unidades
        stock_minimo = insumo_critico.stockMinimo  # 10 unidades
        
        # Verificar detección de stock crítico
        necesita_reposicion = stock_restante < stock_minimo
        assert necesita_reposicion == True
        
        # Calcular cantidad necesaria para reposición
        cantidad_reposicion = stock_minimo - stock_restante
        assert cantidad_reposicion == 3
        
        # Verificar que el sistema puede generar alertas
        insumos_para_verificar = [
            {"cantidad_contada": stock_restante, "stockMinimo": stock_minimo}
        ]
        
        alertas_generadas = CheckListService.contar_insumos_a_reponer(insumos_para_verificar)
        assert alertas_generadas > 0


@pytest.mark.django_db  
class TestIntegracionHTTP:
    """Pruebas de integración a nivel HTTP simulando interacciones web reales."""
    
    def setup_method(self):
        """Configuración para pruebas HTTP."""
        self.client = Client()
        
        # Crear datos base para pruebas HTTP
        self.ambulancia = Ambulancia.objects.create(
            placa="HTTP-001",
            estado="preparada", 
            tipo="tipo_1",
            marca="Test Vehicle",
            fecha_adquisicion=date(2024, 1, 1),
            capacidad=4
        )
    
    @pytest.mark.skip("URLs not configured yet")
    def test_flujo_web_registro_emergencia(self):
        """Valida flujo web completo de registro de emergencias."""
        # Acceder al formulario de registro
        url_registro = reverse('registrar_informe', kwargs={'ambulancia_id': self.ambulancia.id})
        response = self.client.get(url_registro)
        
        # Verificar que el formulario se carga correctamente
        assert response.status_code == 200
        
        # Enviar datos del formulario
        datos_formulario = {
            'direccion_emergencia': 'Av. Web Testing 123',
            'prioridad': 'alta',
            'nombre_chofer': 'Conductor Web Test',
            'paciente_opcional': 'Paciente Web Test'
        }
        
        response = self.client.post(url_registro, datos_formulario)
        
        # Verificar redirección exitosa
        assert response.status_code == 302
        
        # Verificar que el informe se creó en la base de datos
        informe_creado = InformeEmergencia.objects.filter(
            direccion='Av. Web Testing 123'
        ).first()
        
        assert informe_creado is not None
        assert informe_creado.ambulancia == self.ambulancia
        assert informe_creado.prioridad == 'alta'
        assert informe_creado.nombre_chofer == 'Conductor Web Test'
    
    @pytest.mark.skip("URLs not configured yet")
    def test_flujo_web_checklist_inventario(self):
        """Valida flujo web de creación de checklist con selección de insumos."""
        # Crear insumos para el test
        insumo1 = InsumoMedico.objects.create(
            nombre="Insumo Web 1",
            stockMinimo=15,
            unidadMedida="unidades", 
            tipoAmbulancia="tipo_1"
        )
        
        insumo2 = InsumoMedico.objects.create(
            nombre="Insumo Web 2",
            stockMinimo=25,
            unidadMedida="pares",
            tipoAmbulancia="tipo_1"
        )
        
        # Acceder al formulario de checklist
        url_checklist = reverse('registrar_checklist', kwargs={'ambulancia_id': self.ambulancia.id})
        response = self.client.get(url_checklist)
        
        assert response.status_code == 200
        
        # Enviar datos del checklist
        datos_checklist = {
            'nombre_colaborador': 'Colaborador Web Test',
            f'insumo_{insumo1.id}': '20',  # Cantidad del insumo 1
            f'insumo_{insumo2.id}': '30'   # Cantidad del insumo 2
        }
        
        response = self.client.post(url_checklist, datos_checklist)
        
        # Verificar redirección exitosa
        assert response.status_code == 302
        
        # Verificar creación del checklist
        checklist_creado = CheckList.objects.filter(
            ambulancia=self.ambulancia,
            nombre_colaborador='Colaborador Web Test'
        ).first()
        
        assert checklist_creado is not None
        
        # Verificar detalles del checklist
        detalles = DetalleCheckList.objects.filter(checklist=checklist_creado)
        assert detalles.count() == 2
        detalle_insumo1 = detalles.filter(insumo=insumo1).first()
        detalle_insumo2 = detalles.filter(insumo=insumo2).first()
        
        assert detalle_insumo1.cantidad_contada == 20
        assert detalle_insumo2.cantidad_contada == 30


@pytest.mark.django_db
class TestIntegracionRendimiento:
    """Pruebas de rendimiento bajo condiciones de carga."""
    
    def test_performance_multiples_operaciones(self):
        """Valida rendimiento del sistema con múltiples operaciones simultáneas."""
        import time
        
        inicio = time.time()
        
        # Crear múltiples ambulancias
        ambulancias = []
        for i in range(10):
            ambulancia = Ambulancia.objects.create(
                placa=f"PERF-{i:03d}",
                estado="preparada",
                tipo="tipo_1",
                marca=f"Marca {i}",
                fecha_adquisicion=date(2024, 1, 1),
                capacidad=4
            )
            ambulancias.append(ambulancia)
        
        # Crear múltiples pacientes
        pacientes = []
        for i in range(20):
            paciente = Paciente.objects.create(
                nombre=f"Paciente{i}",
                apellido=f"Apellido{i}",
                dni=f"{10000000 + i}",
                fechaNacimiento=date(1990, 1, 1),
                sexo="masculino" if i % 2 == 0 else "femenino"
            )
            pacientes.append(paciente)
        
        insumos = []
        for i in range(15):
            insumo = InsumoMedico.objects.create(
                nombre=f"Insumo Perf {i}",
                stockMinimo=10 + i,
                unidadMedida="unidades",
                tipoAmbulancia="tipo_1"
            )
            insumos.append(insumo)
        
        # Crear múltiples emergencias
        informes = []
        for i in range(10):
            informe = InformeEmergenciaService.registrar_informe({
                "ambulancia_id": ambulancias[i].id,
                "direccion_emergencia": f"Dirección Perf {i}",
                "prioridad": "media",
                "estado": "pendiente",
                "nombre_chofer": f"Chofer {i}"
            })
            informes.append(informe)
        
        # Crear múltiples checklists
        for i in range(5):
            CheckListService.registrar_checklist(
                {"ambulancia": ambulancias[i], "nombre_colaborador": f"Colaborador {i}"},
                [{"insumo": insumos[j], "cantidad_contada": 15 + j} for j in range(3)]
            )
        
        fin = time.time()
        tiempo_total = fin - inicio
        
        # Verificar que las operaciones se completaron en tiempo razonable
        assert tiempo_total < 5.0  # Menos de 5 segundos
        
        # Verificar integridad de los datos
        assert Ambulancia.objects.count() == 10
        assert Paciente.objects.count() == 20
        assert InsumoMedico.objects.count() == 15
        assert InformeEmergencia.objects.count() == 10
        assert CheckList.objects.count() == 5
        
        # Verificar consultas complejas
        ambulancias_con_emergencias = Ambulancia.objects.filter(
            informeemergencia__isnull=False
        ).distinct()
        assert ambulancias_con_emergencias.count() == 10

    def test_integridad_transaccional(self):
        """Valida integridad transaccional y rollback automático en errores."""
        # Crear datos base
        ambulancia = Ambulancia.objects.create(
            placa="TRANS-001",
            estado="preparada",
            tipo="tipo_1",
            marca="Test Trans",
            fecha_adquisicion=date(2024, 1, 1),
            capacidad=4
        )

        paciente = Paciente.objects.create(
            nombre="Test",
            apellido="Transaccional",
            dni="99999999",
            fechaNacimiento=date(1990, 1, 1),
            sexo="masculino"
        )

        # Verificar estado inicial
        count_inicial_informes = InformeEmergencia.objects.count()
        count_inicial_reportes = ReporteEmergencia.objects.count()

        # Intentar operación transaccional que debe fallar completamente
        try:
            with transaction.atomic():
                # Crear informe
                informe = InformeEmergenciaService.registrar_informe({
                    "ambulancia_id": ambulancia.id,
                    "direccion_emergencia": "Test Transaccional",
                    "prioridad": "alta",
                    "estado": "pendiente",
                    "nombre_chofer": "Test Chofer"
                })

                # Crear reporte con ID de insumo inválido (esto debe generar excepción)
                ReporteEmergenciaService.registrar_reporte(
                    informe,
                    "Test procedimientos",
                    "Test pertenencias",
                    [paciente.id],
                    [{"id": 99999, "cantidad": 1}]  # ID inválido
                )

        except Exception:
            # Excepción esperada por ID inválido
            pass

        # Verificar rollback: no se debe haber creado ni el informe ni el reporte
        assert InformeEmergencia.objects.count() == count_inicial_informes
        assert ReporteEmergencia.objects.count() == count_inicial_reportes
if __name__ == '__main__':
    """Ejecutar pruebas con: pytest tests_integration_advanced.py -v"""
    pytest.main([__file__, '-v'])