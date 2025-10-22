from django.db import models

# Create your models here.

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8, unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fechaNacimiento = models.DateField()
    SEXO_PAC = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')]
    sexo = models.CharField(max_length=20, choices=SEXO_PAC)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.dni}"
    
class HistorialMedico(models.Model):
    alergias = models.TextField(blank=True, null=True)
    tipoSangre = models.CharField(max_length=5)
    enfermedades = models.TextField(blank=True, null=True)
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historial_medico')
    
    def __str__(self):
        return f"Historial Médico de {self.paciente.nombre} - Tipo: {self.tipoSangre}"