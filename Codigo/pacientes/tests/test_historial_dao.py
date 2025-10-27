from django.test import TestCase
from datetime import date
from pacientes.models import Paciente, HistorialMedico
from pacientes.dao.historial_dao import HistorialDAO


class HistorialDAOTest(TestCase):
    """Test suite for HistorialDAO"""
    
    def setUp(self):
        """Set up test data"""
        self.dao = HistorialDAO()
        self.paciente = Paciente.objects.create(
            nombre='Roberto',
            apellido='Sánchez',
            dni='44444444',
            fechaNacimiento=date(1975, 9, 5),
            sexo='masculino'
        )
        self.historial = HistorialMedico.objects.create(
            alergias='Polen',
            tipoSangre='O-',
            enfermedades='Hipertensión',
            paciente=self.paciente
        )
    
    def test_obtener_por_paciente_existente(self):
        """Test retrieving historial for paciente with existing historial"""
        historial = self.dao.obtener_por_paciente(self.paciente)
        
        self.assertIsNotNone(historial)
        self.assertEqual(historial.tipoSangre, 'O-')
        self.assertEqual(historial.alergias, 'Polen')
        self.assertEqual(historial.enfermedades, 'Hipertensión')
    
    def test_obtener_por_paciente_sin_historial(self):
        """Test retrieving historial for paciente without historial"""
        new_paciente = Paciente.objects.create(
            nombre='Maria',
            apellido='García',
            dni='55555555',
            fechaNacimiento=date(1990, 3, 15),
            sexo='femenino'
        )
        
        historial = self.dao.obtener_por_paciente(new_paciente)
        self.assertIsNone(historial)
    
    def test_crear_historial(self):
        """Test creating a new historial medico"""
        new_paciente = Paciente.objects.create(
            nombre='Sofia',
            apellido='Torres',
            dni='66666666',
            fechaNacimiento=date(1990, 12, 12),
            sexo='femenino'
        )
        
        historial_data = {
            'tipoSangre': 'A+',
            'alergias': 'Ninguna',
            'enfermedades': 'Ninguna'
        }
        
        historial = self.dao.crear_historial(new_paciente, historial_data)
        
        self.assertIsNotNone(historial.id)
        self.assertEqual(historial.tipoSangre, 'A+')
        self.assertEqual(historial.alergias, 'Ninguna')
        self.assertEqual(historial.paciente, new_paciente)
        
        # Verify it's in database
        db_historial = HistorialMedico.objects.get(paciente=new_paciente)
        self.assertEqual(db_historial.tipoSangre, 'A+')
    
    def test_crear_historial_campos_opcionales(self):
        """Test creating historial with optional fields only"""
        new_paciente = Paciente.objects.create(
            nombre='Luis',
            apellido='Morales',
            dni='77777777',
            fechaNacimiento=date(1985, 5, 5),
            sexo='masculino'
        )
        
        historial_data = {
            'tipoSangre': 'B+'
        }
        
        historial = self.dao.crear_historial(new_paciente, historial_data)
        
        self.assertIsNotNone(historial.id)
        self.assertEqual(historial.tipoSangre, 'B+')
        self.assertIsNone(historial.alergias)
        self.assertIsNone(historial.enfermedades)
    
    def test_actualizar_historial(self):
        """Test updating historial information"""
        update_data = {
            'enfermedades': 'Hipertensión, Diabetes',
            'alergias': 'Polen, Ácaros'
        }
        
        updated = self.dao.actualizar_historial(self.historial, update_data)
        
        self.assertIn('Diabetes', updated.enfermedades)
        self.assertIn('Ácaros', updated.alergias)
        # Verify tipoSangre unchanged
        self.assertEqual(updated.tipoSangre, 'O-')
        
        # Verify changes persisted to database
        db_historial = HistorialMedico.objects.get(id=self.historial.id)
        self.assertIn('Diabetes', db_historial.enfermedades)
    
    def test_actualizar_historial_tipo_sangre(self):
        """Test updating blood type in historial"""
        update_data = {'tipoSangre': 'AB+'}
        
        updated = self.dao.actualizar_historial(self.historial, update_data)
        
        self.assertEqual(updated.tipoSangre, 'AB+')
        # Verify other fields unchanged
        self.assertEqual(updated.alergias, 'Polen')
        self.assertEqual(updated.enfermedades, 'Hipertensión')
