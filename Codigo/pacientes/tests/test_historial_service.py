from django.test import TestCase
from datetime import date
from pacientes.models import Paciente, HistorialMedico
from pacientes.services.historial_service import HistorialService


class HistorialServiceTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.service = HistorialService()
        self.paciente = Paciente.objects.create(
            nombre='Elena',
            apellido='Ramírez',
            dni='88888888',
            fechaNacimiento=date(1987, 4, 25),
            sexo='femenino'
        )
        self.historial = HistorialMedico.objects.create(
            tipoSangre='AB-',
            alergias='Ninguna',
            paciente=self.paciente
        )
    
    def test_buscar_historial_por_dni(self):
        """Test searching historial by DNI"""
        paciente, historial = self.service.buscar_historial(dni='88888888')
        
        self.assertIsNotNone(paciente)
        self.assertIsNotNone(historial)
        self.assertEqual(paciente.nombre, 'Elena')
        self.assertEqual(historial.tipoSangre, 'AB-')
    
    def test_buscar_historial_por_nombre(self):
        """Test searching historial by name"""
        paciente, historial = self.service.buscar_historial(nombre='Elena')
        
        self.assertIsNotNone(paciente)
        self.assertIsNotNone(historial)
        self.assertEqual(paciente.dni, '88888888')
        self.assertEqual(historial.tipoSangre, 'AB-')
    
    def test_buscar_historial_paciente_sin_historial(self):
        """Test searching historial for paciente without historial"""
        new_paciente = Paciente.objects.create(
            nombre='Diego',
            apellido='Vargas',
            dni='99999999',
            fechaNacimiento=date(1992, 8, 10),
            sexo='masculino'
        )
        
        paciente, historial = self.service.buscar_historial(dni='99999999')
        
        self.assertIsNotNone(paciente)
        self.assertIsNone(historial)
    
    def test_buscar_historial_paciente_no_existe(self):
        """Test searching historial for non-existent paciente"""
        paciente, historial = self.service.buscar_historial(dni='00000000')
        
        self.assertIsNone(paciente)
        self.assertIsNone(historial)
    
    def test_registrar_historial_completo(self):
        """Test registering new paciente with historial"""
        datos_paciente = {
            'nombre': 'Carmen',
            'apellido': 'Flores',
            'dni': '12121212',
            'fechaNacimiento': date(1993, 6, 15),
            'sexo': 'femenino',
            'email': 'carmen@example.com'
        }
        
        datos_historial = {
            'tipoSangre': 'O+',
            'alergias': 'Penicilina',
            'enfermedades': 'Ninguna'
        }
        
        paciente, historial = self.service.registrar_historial(
            datos_paciente, datos_historial
        )
        
        self.assertIsNotNone(paciente.id)
        self.assertIsNotNone(historial.id)
        self.assertEqual(paciente.nombre, 'Carmen')
        self.assertEqual(paciente.dni, '12121212')
        self.assertEqual(historial.tipoSangre, 'O+')
        self.assertEqual(historial.alergias, 'Penicilina')
        self.assertEqual(historial.paciente, paciente)
        
        # Verify in database
        db_paciente = Paciente.objects.get(dni='12121212')
        self.assertEqual(db_paciente.nombre, 'Carmen')
        self.assertEqual(db_paciente.historial_medico.tipoSangre, 'O+')
    
    def test_actualizar_historial_existente(self):
        """Test updating existing paciente and historial"""
        datos_paciente = {
            'telefono': '123456789',
            'email': 'elena.updated@example.com'
        }
        
        datos_historial = {
            'alergias': 'Polen, Penicilina',
            'enfermedades': 'Asma'
        }
        
        paciente, historial = self.service.actualizar_historial(
            self.paciente.id, datos_paciente, datos_historial
        )
        
        self.assertEqual(paciente.telefono, '123456789')
        self.assertEqual(paciente.email, 'elena.updated@example.com')
        self.assertEqual(historial.alergias, 'Polen, Penicilina')
        self.assertEqual(historial.enfermedades, 'Asma')
        # Verify unchanged fields
        self.assertEqual(paciente.nombre, 'Elena')
        self.assertEqual(historial.tipoSangre, 'AB-')
    
    def test_actualizar_crear_historial_si_no_existe(self):
        """Test updating paciente and creating historial if it doesn't exist"""
        new_paciente = Paciente.objects.create(
            nombre='Fernando',
            apellido='Ruiz',
            dni='13131313',
            fechaNacimiento=date(1988, 9, 20),
            sexo='masculino'
        )
        
        datos_paciente = {'telefono': '987654321'}
        datos_historial = {
            'tipoSangre': 'A-',
            'alergias': 'Mariscos'
        }
        
        paciente, historial = self.service.actualizar_historial(
            new_paciente.id, datos_paciente, datos_historial
        )
        
        self.assertEqual(paciente.telefono, '987654321')
        self.assertIsNotNone(historial)
        self.assertEqual(historial.tipoSangre, 'A-')
        self.assertEqual(historial.alergias, 'Mariscos')
        
        # Verify historial was created in database
        db_paciente = Paciente.objects.get(id=new_paciente.id)
        self.assertTrue(hasattr(db_paciente, 'historial_medico'))
        self.assertEqual(db_paciente.historial_medico.tipoSangre, 'A-')
    
    def test_registrar_historial_solo_campos_requeridos(self):
        """Test registering with only required fields"""
        datos_paciente = {
            'nombre': 'Jose',
            'apellido': 'Silva',
            'dni': '14141414',
            'fechaNacimiento': date(1991, 11, 11),
            'sexo': 'masculino'
        }
        
        datos_historial = {
            'tipoSangre': 'B-'
        }
        
        paciente, historial = self.service.registrar_historial(
            datos_paciente, datos_historial
        )
        
        self.assertIsNotNone(paciente)
        self.assertIsNotNone(historial)
        self.assertEqual(historial.tipoSangre, 'B-')
        self.assertIsNone(historial.alergias)
        self.assertIsNone(historial.enfermedades)
