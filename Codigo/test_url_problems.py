import pytest
from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from datetime import date

from ambulancias.models import Ambulancia
from emergencias.models import InformeEmergencia
from pacientes.models import Paciente

@pytest.mark.django_db
class TestURLReverseMatch:
    """Pruebas para detectar problemas de NoReverseMatch en URLs."""
    
    def setup_method(self):
        """Configuración de datos base para pruebas de URLs."""
        self.client = Client()
        
        # Crear datos de prueba
        self.ambulancia = Ambulancia.objects.create(
            placa="URL-001",
            estado="preparada",
            tipo="tipo_1", 
            marca="Test URL",
            fecha_adquisicion=date(2024, 1, 1),
            capacidad=4
        )
        
        self.paciente = Paciente.objects.create(
            nombre="Test",
            apellido="URL",
            dni="12345678",
            fechaNacimiento=date(1990, 1, 1),
            sexo="masculino"
        )
        
        self.informe = InformeEmergencia.objects.create(
            ambulancia=self.ambulancia,
            direccion="Test URL Direction",
            prioridad="media",
            estado="pendiente",
            nombre_chofer="Test Driver"
        )

    def test_urls_principales_existen(self):
        """Verificar que las URLs principales estén configuradas correctamente."""
        urls_principales = [
            'core:home',
            'ambulancias:listar_ambulancias', 
            'ambulancias:registrar_ambulancia',
            'ambulancias:submenu_ambulancias',
            'emergencias:listar_informes_emergencia',
        ]
        
        for url_name in urls_principales:
            try:
                url = reverse(url_name)
                assert url is not None
                print(f"{url_name} -> {url}")
            except NoReverseMatch as e:
                pytest.fail(f"NoReverseMatch para {url_name}: {e}")

    def test_urls_con_parametros_existen(self):
        """Verificar URLs que requieren parámetros."""
        urls_con_parametros = [
            ('ambulancias:editar_ambulancia', {'id': self.ambulancia.id}),
            ('emergencias:registrar_informe', {'ambulancia_id': self.ambulancia.id}),
            ('emergencias:detalles_informe', {'informe_id': self.informe.id}),
            ('emergencias:generar_revocacion', {'id': self.informe.id}),
            ('emergencias:generar_consentimiento', {'id': self.informe.id}),
            ('emergencias:generar_reporte_emergencia', {'id': self.informe.id}),
        ]
        
        for url_name, kwargs in urls_con_parametros:
            try:
                url = reverse(url_name, kwargs=kwargs)
                assert url is not None
                print(f"{url_name} con {kwargs} -> {url}")
            except NoReverseMatch as e:
                pytest.fail(f"NoReverseMatch para {url_name} con {kwargs}: {e}")

    def test_urls_ambulancias_completas(self):
        """Probar todas las URLs del módulo ambulancias."""
        urls_ambulancias = [
            ('ambulancias:listar_ambulancias', None),
            ('ambulancias:registrar_ambulancia', None),
            ('ambulancias:submenu_ambulancias', None),
            ('ambulancias:editar_ambulancia', {'id': self.ambulancia.id}),
            ('ambulancias:lista_averias', None),
            ('ambulancias:registrar_averia', None),
            ('ambulancias:lista_combustible', None),
            ('ambulancias:registrar_combustible', None),
        ]
        
        for url_name, kwargs in urls_ambulancias:
            try:
                if kwargs:
                    url = reverse(url_name, kwargs=kwargs)
                else:
                    url = reverse(url_name)
                assert url is not None
                print(f"{url_name} -> {url}")
            except NoReverseMatch as e:
                pytest.fail(f"NoReverseMatch en ambulancias para {url_name}: {e}")

    def test_urls_emergencias_completas(self):
        """Probar todas las URLs del módulo emergencias."""
        urls_emergencias = [
            ('emergencias:listar_informes_emergencia', None),
            ('emergencias:registrar_informe', {'ambulancia_id': self.ambulancia.id}),
            ('emergencias:lista_informes_pacientes', None),
            ('emergencias:asignar_ambulancia', None),
            ('emergencias:detalles_informe', {'informe_id': self.informe.id}),
            ('emergencias:generar_revocacion', {'id': self.informe.id}),
            ('emergencias:generar_consentimiento', {'id': self.informe.id}),
            ('emergencias:generar_reporte_emergencia', {'id': self.informe.id}),
        ]
        
        for url_name, kwargs in urls_emergencias:
            try:
                if kwargs:
                    url = reverse(url_name, kwargs=kwargs)
                else:
                    url = reverse(url_name)
                assert url is not None
                print(f"{url_name} -> {url}")
            except NoReverseMatch as e:
                pytest.fail(f"NoReverseMatch en emergencias para {url_name}: {e}")

    def test_acceso_http_urls_principales(self):
        """Verificar que las URLs principales respondan HTTP correctamente."""
        urls_accesibles = [
            reverse('core:home'),
            reverse('ambulancias:listar_ambulancias'),
            reverse('ambulancias:submenu_ambulancias'),
            reverse('emergencias:listar_informes_emergencia'),
        ]
        
        for url in urls_accesibles:
            response = self.client.get(url)
            # Aceptar 200 (OK), 302 (Redirect), 404 (Not Found)
            # pero NO 500 (Server Error) que indicaría problema de código
            assert response.status_code in [200, 302, 404], \
                f"URL {url} devuelve error 500: problema en vista o template"

    def test_urls_con_parametros_incorrectos(self):
        """Verificar manejo de parámetros incorrectos."""
        # Estos DEBEN fallar con NoReverseMatch
        urls_incorrectas = [
            ('ambulancias:editar_ambulancia', {}),  # Falta 'id'
            ('emergencias:detalles_informe', {}),   # Falta 'informe_id'
            ('emergencias:generar_revocacion', {}), # Falta 'id'
        ]
        
        for url_name, kwargs in urls_incorrectas:
            with pytest.raises(NoReverseMatch):
                reverse(url_name, kwargs=kwargs)
                print(f"{url_name} correctamente falló sin parámetros")

    def test_deteccion_urls_duplicadas(self):
        """Detectar URLs duplicadas que pueden causar conflictos."""
        # Verificar que no hay duplicados en emergencias
        # Hay dos 'registrar_informe' con diferentes parámetros
        
        try:
            # Esta debería funcionar con parámetros
            url1 = reverse('emergencias:registrar_informe', kwargs={'ambulancia_id': 1})
            
            # Esta podría causar conflicto si no está bien configurada
            # Como ambas tienen el mismo nombre, Django puede confundirse
            assert url1 is not None
            
            # Verificar que las URLs son diferentes según parámetros
            url2 = reverse('emergencias:registrar_informe', kwargs={'ambulancia_id': 2})
            assert url1 != url2  # Deben ser URLs diferentes
            
        except NoReverseMatch as e:
            pytest.fail(f"Conflicto de URLs duplicadas: {e}")

    def test_urls_inventarios_y_pacientes(self):
        """Verificar URLs de módulos inventarios y pacientes si existen."""
        try:
            # Intentar acceder a URLs de inventarios
            from inventarios.urls import urlpatterns as inv_urls
            assert len(inv_urls) > 0, "Módulo inventarios debe tener URLs"
            
        except ImportError:
            pytest.skip("Módulo inventarios no tiene URLs configuradas")
        
        try:
            # Intentar acceder a URLs de pacientes  
            from pacientes.urls import urlpatterns as pac_urls
            assert len(pac_urls) > 0, "Módulo pacientes debe tener URLs"
            
        except ImportError:
            pytest.skip("Módulo pacientes no tiene URLs configuradas")

@pytest.mark.django_db
class TestTemplateURLTags:
    """Pruebas para detectar problemas con tags {% url %} en templates."""
    
    def setup_method(self):
        self.client = Client()
        self.ambulancia = Ambulancia.objects.create(
            placa="TPL-001",
            estado="preparada",
            tipo="tipo_1",
            marca="Template Test",
            fecha_adquisicion=date(2024, 1, 1),
            capacidad=4
        )
        
    def test_renderizado_templates_sin_errores(self):
        """Verificar que los templates se renderizan sin NoReverseMatch."""
        urls_con_templates = [
            reverse('core:home'),
            reverse('ambulancias:listar_ambulancias'),
            reverse('emergencias:listar_informes_emergencia'),
        ]
        
        for url in urls_con_templates:
            response = self.client.get(url)
            
            # Si hay NoReverseMatch en template, será error 500
            if response.status_code == 500:
                pytest.fail(f"Template en {url} tiene NoReverseMatch en url tags")
            
            print(f"Template en {url} renderiza correctamente (status: {response.status_code})")
    
    def test_post_registrar_ambulancia(self):
        """Test POST para registrar ambulancia desde formulario"""
        url = reverse('ambulancias:registrar_ambulancia')
        data = {
            'placa': 'POST-001',
            'estado': 'Disponible',
            'tipo_A': 'Tipo I',
            'marca': 'Toyota',
            'fecha_adquisicion': '2024-11-22'
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        assert Ambulancia.objects.filter(placa='POST-001').exists()
    
    def test_post_registrar_informe(self):
        """Test POST para registrar informe de emergencia"""
        url = reverse('emergencias:registrar_informe', kwargs={'ambulancia_id': self.ambulancia.id})
        data = {
            'direccion': 'Av Test 123',
            'prioridad': 'alta',
            'estado': 'pendiente',
            'nombre_chofer': 'Test Driver'
        }
        response = self.client.post(url, data)
        assert response.status_code in [200, 302]  # Puede requerir autenticación
    
    def test_filtros_ambulancias(self):
        """Test filtros en listado de ambulancias"""
        url = reverse('ambulancias:listar_ambulancias')
        response = self.client.get(url, {'estado': 'preparada'})
        assert response.status_code == 200
        assert 'ambulancias' in response.context
    
    def test_busqueda_paciente(self):
        """Test búsqueda de paciente"""
        Paciente.objects.create(
            nombre="Test",
            apellido="Search",
            dni="99999999",
            fechaNacimiento=date(1990, 1, 1),
            sexo="M"
        )
        url = reverse('pacientes:historial_busqueda')
        response = self.client.get(url, {'dni': '99999999'})
        assert response.status_code == 200

if __name__ == '__main__':
    """Ejecutar con: pytest test_url_problems.py -v"""
    pytest.main([__file__, '-v', '-s'])