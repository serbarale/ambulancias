from django.test import TestCase
from datetime import date
from pacientes.models import Paciente
from pacientes.dao.paciente_dao import PacienteDAO


class PacienteDAOTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.dao = PacienteDAO()
        self.paciente1 = Paciente.objects.create(
            nombre='Ana',
            apellido='Martínez',
            dni='11111111',
            fechaNacimiento=date(1992, 1, 1),
            sexo='femenino',
            email='ana@example.com'
        )
        self.paciente2 = Paciente.objects.create(
            nombre='Pedro',
            apellido='López',
            dni='22222222',
            fechaNacimiento=date(1988, 6, 15),
            sexo='masculino',
            telefono='999888777'
        )
    
    def test_buscar_por_dni_encontrado(self):
        """Test searching paciente by DNI - found"""
        paciente = self.dao.buscar_por_dni_o_nombre(dni='11111111')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nombre, 'Ana')
        self.assertEqual(paciente.dni, '11111111')
    
    def test_buscar_por_dni_no_encontrado(self):
        """Test searching paciente by DNI - not found"""
        paciente = self.dao.buscar_por_dni_o_nombre(dni='99999999')
        self.assertIsNone(paciente)
    
    def test_buscar_por_dni_parcial(self):
        """Test searching paciente by partial DNI"""
        paciente = self.dao.buscar_por_dni_o_nombre(dni='1111')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.dni, '11111111')
    
    def test_buscar_por_nombre_encontrado(self):
        """Test searching paciente by name - found"""
        paciente = self.dao.buscar_por_dni_o_nombre(nombre='Pedro')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nombre, 'Pedro')
    
    def test_buscar_por_nombre_no_encontrado(self):
        """Test searching paciente by name - not found"""
        paciente = self.dao.buscar_por_dni_o_nombre(nombre='Carlos')
        self.assertIsNone(paciente)
    
    def test_buscar_por_nombre_parcial(self):
        """Test searching paciente by partial name"""
        paciente = self.dao.buscar_por_dni_o_nombre(nombre='Ped')
        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nombre, 'Pedro')
    
    def test_buscar_sin_parametros(self):
        """Test searching without parameters returns None"""
        paciente = self.dao.buscar_por_dni_o_nombre()
        self.assertIsNone(paciente)
    
    def test_crear_paciente(self):
        """Test creating a new paciente"""
        paciente_data = {
            'nombre': 'Laura',
            'apellido': 'Fernández',
            'dni': '33333333',
            'fechaNacimiento': date(1995, 3, 20),
            'sexo': 'femenino',
            'email': 'laura@example.com'
        }
        paciente = self.dao.crear_paciente(paciente_data)
        
        self.assertIsNotNone(paciente.id)
        self.assertEqual(paciente.nombre, 'Laura')
        self.assertEqual(paciente.apellido, 'Fernández')
        self.assertEqual(paciente.dni, '33333333')
        
        # Verify it's in database
        db_paciente = Paciente.objects.get(dni='33333333')
        self.assertEqual(db_paciente.nombre, 'Laura')
    
    def test_actualizar_paciente(self):
        """Test updating paciente information"""
        update_data = {
            'telefono': '111222333',
            'email': 'ana.updated@example.com'
        }
        updated = self.dao.actualizar_paciente(self.paciente1, update_data)
        
        self.assertEqual(updated.telefono, '111222333')
        self.assertEqual(updated.email, 'ana.updated@example.com')
        # Verify original data remains
        self.assertEqual(updated.nombre, 'Ana')
        self.assertEqual(updated.dni, '11111111')
        
        # Verify changes persisted to database
        db_paciente = Paciente.objects.get(id=self.paciente1.id)
        self.assertEqual(db_paciente.telefono, '111222333')
    
    def test_actualizar_paciente_nombre(self):
        """Test updating paciente name"""
        update_data = {'nombre': 'Anabel'}
        updated = self.dao.actualizar_paciente(self.paciente1, update_data)
        
        self.assertEqual(updated.nombre, 'Anabel')
        self.assertEqual(updated.apellido, 'Martínez')  # Unchanged
