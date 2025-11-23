import pytest
from django.db import IntegrityError
from datetime import date
from pacientes.models import Paciente, HistorialMedico


@pytest.mark.django_db
class TestPacienteModel:
    """Test suite for Paciente model"""
    
    @pytest.fixture
    def paciente_data(self):
        """Fixture for basic patient data"""
        return {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'dni': '12345678',
            'direccion': 'Calle Falsa 123',
            'email': 'juan.perez@example.com',
            'telefono': '987654321',
            'fechaNacimiento': date(1990, 5, 15),
            'sexo': 'masculino'
        }
    
    def test_create_paciente(self, paciente_data):
        """Test creating a Paciente instance with all fields"""
        paciente = Paciente.objects.create(**paciente_data)
        assert paciente.nombre == 'Juan'
        assert paciente.apellido == 'Pérez'
        assert paciente.dni == '12345678'
        assert paciente.sexo == 'masculino'
        assert paciente.email == 'juan.perez@example.com'
        assert paciente.telefono == '987654321'
        assert paciente.direccion == 'Calle Falsa 123'
    
    def test_paciente_str_method(self, paciente_data):
        """Test Paciente __str__ method returns correct format"""
        paciente = Paciente.objects.create(**paciente_data)
        expected_str = "Pérez, Juan - 12345678"
        assert str(paciente) == expected_str
    
    def test_dni_unique_constraint(self, paciente_data):
        """Test that DNI must be unique"""
        Paciente.objects.create(**paciente_data)
        # Try to create another paciente with same DNI
        with pytest.raises(IntegrityError):
            Paciente.objects.create(**paciente_data)
    
    def test_paciente_optional_fields(self):
        """Test creating Paciente with only required fields"""
        paciente = Paciente.objects.create(
            nombre='María',
            apellido='González',
            dni='87654321',
            fechaNacimiento=date(1985, 3, 20),
            sexo='femenino'
        )
        assert paciente.direccion is None
        assert paciente.email is None
        assert paciente.telefono is None
    
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
        assert paciente_m.sexo == 'masculino'
        
        # Test femenino
        paciente_f = Paciente.objects.create(
            nombre='Ana',
            apellido='Martínez',
            dni='22222222',
            fechaNacimiento=date(1985, 2, 2),
            sexo='femenino'
        )
        assert paciente_f.sexo == 'femenino'


@pytest.mark.django_db
class TestHistorialMedicoModel:
    """Test suite for HistorialMedico model"""
    
    @pytest.fixture
    def paciente_base(self):
        """Fixture for base patient"""
        return Paciente.objects.create(
            nombre='Carlos',
            apellido='Rodríguez',
            dni='11223344',
            fechaNacimiento=date(1980, 7, 10),
            sexo='masculino'
        )
    
    def test_create_historial_medico(self, paciente_base):
        """Test creating a HistorialMedico instance"""
        historial = HistorialMedico.objects.create(
            alergias='Penicilina',
            tipoSangre='O+',
            enfermedades='Diabetes',
            paciente=paciente_base
        )
        assert historial.tipoSangre == 'O+'
        assert historial.alergias == 'Penicilina'
        assert historial.enfermedades == 'Diabetes'
        assert historial.paciente == paciente_base
    
    def test_historial_str_method(self, paciente_base):
        """Test HistorialMedico __str__ method returns correct format"""
        historial = HistorialMedico.objects.create(
            tipoSangre='A+',
            paciente=paciente_base
        )
        expected_str = f"Historial Médico de {paciente_base.nombre} - Tipo: A+"
        assert str(historial) == expected_str
    
    def test_one_to_one_relationship(self, paciente_base):
        """Test OneToOne relationship between Paciente and HistorialMedico"""
        historial = HistorialMedico.objects.create(
            tipoSangre='B-',
            paciente=paciente_base
        )
        # Access historial from paciente using related_name
        assert paciente_base.historial_medico == historial
    
    def test_cascade_delete(self, paciente_base):
        """Test that HistorialMedico is deleted when Paciente is deleted"""
        historial = HistorialMedico.objects.create(
            tipoSangre='AB+',
            paciente=paciente_base
        )
        historial_id = historial.id
        
        # Delete paciente
        paciente_base.delete()
        
        # Verify historial was also deleted
        with pytest.raises(HistorialMedico.DoesNotExist):
            HistorialMedico.objects.get(id=historial_id)
    
    def test_historial_optional_fields(self, paciente_base):
        """Test creating HistorialMedico with only required fields"""
        historial = HistorialMedico.objects.create(
            tipoSangre='O-',
            paciente=paciente_base
        )
        assert historial.alergias is None
        assert historial.enfermedades is None
        assert historial.tipoSangre == 'O-'
