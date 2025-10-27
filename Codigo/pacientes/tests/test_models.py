from django.test import TestCase
from django.db import IntegrityError
from datetime import date
from pacientes.models import Paciente, HistorialMedico


class PacienteModelTest(TestCase):
    """Test suite for Paciente model"""
    
    def setUp(self):
        """Set up test data"""
        self.paciente_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'dni': '12345678',
            'direccion': 'Calle Falsa 123',
            'email': 'juan.perez@example.com',
            'telefono': '987654321',
            'fechaNacimiento': date(1990, 5, 15),
            'sexo': 'masculino'
        }
    
    def test_create_paciente(self):
        """Test creating a Paciente instance with all fields"""
        paciente = Paciente.objects.create(**self.paciente_data)
        self.assertEqual(paciente.nombre, 'Juan')
        self.assertEqual(paciente.apellido, 'Pérez')
        self.assertEqual(paciente.dni, '12345678')
        self.assertEqual(paciente.sexo, 'masculino')
        self.assertEqual(paciente.email, 'juan.perez@example.com')
        self.assertEqual(paciente.telefono, '987654321')
        self.assertEqual(paciente.direccion, 'Calle Falsa 123')
    
    def test_paciente_str_method(self):
        """Test Paciente __str__ method returns correct format"""
        paciente = Paciente.objects.create(**self.paciente_data)
        expected_str = "Pérez, Juan - 12345678"
        self.assertEqual(str(paciente), expected_str)
    
    def test_dni_unique_constraint(self):
        """Test that DNI must be unique"""
        Paciente.objects.create(**self.paciente_data)
        # Try to create another paciente with same DNI
        with self.assertRaises(IntegrityError):
            Paciente.objects.create(**self.paciente_data)
    
    def test_paciente_optional_fields(self):
        """Test creating Paciente with only required fields"""
        paciente = Paciente.objects.create(
            nombre='María',
            apellido='González',
            dni='87654321',
            fechaNacimiento=date(1985, 3, 20),
            sexo='femenino'
        )
        self.assertIsNone(paciente.direccion)
        self.assertIsNone(paciente.email)
        self.assertIsNone(paciente.telefono)
    
    def test_paciente_sexo_choices(self):
        """Test that sexo field accepts valid choices"""
        # Test masculino
        paciente_m = Paciente.objects.create(
            nombre='Carlos',
            apellido='López',
            dni='11111111',
            fechaNacimiento=date(1980, 1, 1),
            sexo='masculino'
        )
        self.assertEqual(paciente_m.sexo, 'masculino')
        
        # Test femenino
        paciente_f = Paciente.objects.create(
            nombre='Ana',
            apellido='Martínez',
            dni='22222222',
            fechaNacimiento=date(1985, 2, 2),
            sexo='femenino'
        )
        self.assertEqual(paciente_f.sexo, 'femenino')


class HistorialMedicoModelTest(TestCase):
    """Test suite for HistorialMedico model"""
    
    def setUp(self):
        """Set up test data"""
        self.paciente = Paciente.objects.create(
            nombre='Carlos',
            apellido='Rodríguez',
            dni='11223344',
            fechaNacimiento=date(1980, 7, 10),
            sexo='masculino'
        )
    
    def test_create_historial_medico(self):
        """Test creating a HistorialMedico instance"""
        historial = HistorialMedico.objects.create(
            alergias='Penicilina',
            tipoSangre='O+',
            enfermedades='Diabetes',
            paciente=self.paciente
        )
        self.assertEqual(historial.tipoSangre, 'O+')
        self.assertEqual(historial.alergias, 'Penicilina')
        self.assertEqual(historial.enfermedades, 'Diabetes')
        self.assertEqual(historial.paciente, self.paciente)
    
    def test_historial_str_method(self):
        """Test HistorialMedico __str__ method returns correct format"""
        historial = HistorialMedico.objects.create(
            tipoSangre='A+',
            paciente=self.paciente
        )
        expected_str = f"Historial Médico de {self.paciente.nombre} - Tipo: A+"
        self.assertEqual(str(historial), expected_str)
    
    def test_one_to_one_relationship(self):
        """Test OneToOne relationship between Paciente and HistorialMedico"""
        historial = HistorialMedico.objects.create(
            tipoSangre='B-',
            paciente=self.paciente
        )
        # Access historial from paciente using related_name
        self.assertEqual(self.paciente.historial_medico, historial)
    
    def test_cascade_delete(self):
        """Test that HistorialMedico is deleted when Paciente is deleted"""
        historial = HistorialMedico.objects.create(
            tipoSangre='AB+',
            paciente=self.paciente
        )
        historial_id = historial.id
        
        # Delete paciente
        self.paciente.delete()
        
        # Verify historial was also deleted
        with self.assertRaises(HistorialMedico.DoesNotExist):
            HistorialMedico.objects.get(id=historial_id)
    
    def test_historial_optional_fields(self):
        """Test creating HistorialMedico with only required fields"""
        historial = HistorialMedico.objects.create(
            tipoSangre='O-',
            paciente=self.paciente
        )
        self.assertIsNone(historial.alergias)
        self.assertIsNone(historial.enfermedades)
        self.assertEqual(historial.tipoSangre, 'O-')
