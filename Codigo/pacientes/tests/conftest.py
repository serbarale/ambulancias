import pytest
from datetime import date
from pacientes.models import Paciente, HistorialMedico

@pytest.fixture
def paciente_base():
    """Fixture para crear un paciente básico"""
    return Paciente.objects.create(
        nombre='Juan',
        apellido='Pérez',
        dni='12345678',
        fechaNacimiento=date(1990, 5, 15),
        sexo='masculino',
        direccion='Calle Falsa 123',
        email='juan.perez@example.com',
        telefono='987654321'
    )

@pytest.fixture
def historial_base(paciente_base):
    """Fixture para crear un historial médico básico"""
    return HistorialMedico.objects.create(
        paciente=paciente_base,
        tipoSangre='O+',
        alergias='Ninguna',
        enfermedades='Ninguna'
    )

@pytest.fixture
def paciente_service_data():
    """Fixture con datos para pruebas de servicio"""
    return {
        'datos_paciente': {
            'nombre': 'Carmen',
            'apellido': 'Flores',
            'dni': '12121212',
            'fechaNacimiento': date(1993, 6, 15),
            'sexo': 'femenino',
            'email': 'carmen@example.com'
        },
        'datos_historial': {
            'tipoSangre': 'O+',
            'alergias': 'Penicilina',
            'enfermedades': 'Ninguna'
        }
    }