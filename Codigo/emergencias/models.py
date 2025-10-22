from django.db import models
from ambulancias.models import Ambulancia
from pacientes.models import Paciente
from inventarios.models import InsumoMedico

# Create your models here.

class InformeEmergencia(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]

    PRIORIDADES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    ambulancia = models.ForeignKey(Ambulancia, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    nombre_chofer = models.CharField(max_length=100)
    paciente_opcional = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.direccion} - {self.prioridad} - {self.fecha_registro.strftime('%d/%m/%Y %H:%M')}"

class FormatoRevocacion(models.Model):
    TIPO_PERSONA = [
        ('paciente', 'Paciente'),
        ('responsable', 'Responsable Legal'),
    ]

    TIPO_DOCUMENTO = [
        ('dni', 'DNI'),
        ('ce', 'Carnet de extranjería'),
        ('pasaporte', 'Pasaporte'),
    ]

    informe = models.OneToOneField(InformeEmergencia, on_delete=models.CASCADE)
    nombre_declarante = models.CharField(max_length=100)
    tipo_persona = models.CharField(max_length=20, choices=TIPO_PERSONA)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20)
    motivo_revocacion = models.TextField()
    nombre_testigo = models.CharField(max_length=100)
    fecha_firma = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Revocación - {self.nombre_declarante} ({self.fecha_firma})"
    
class FormatoConsentimiento(models.Model):
    informe = models.OneToOneField(InformeEmergencia, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=100)
    nombre_paciente = models.CharField(max_length=100)
    dni_paciente = models.CharField(max_length=12)
    personal_medico = models.CharField(max_length=100)
    acepta_acto_medico = models.BooleanField(default=False)
    acepta_traslado = models.BooleanField(default=False)
    fecha_firma = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Consentimiento de {self.nombre_paciente} - {self.informe}"

class ReporteEmergencia(models.Model):
    informe = models.OneToOneField(InformeEmergencia, on_delete=models.CASCADE)
    procedimientos = models.TextField()
    pertenencias = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte - {self.informe}"
    
class ReportePaciente(models.Model):
    reporte = models.ForeignKey(ReporteEmergencia, on_delete=models.CASCADE, related_name='pacientes')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paciente} en {self.reporte}"

class InsumoUtilizado(models.Model):
    reporte = models.ForeignKey(ReporteEmergencia, on_delete=models.CASCADE, related_name='insumos')
    insumo = models.ForeignKey(InsumoMedico, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad} de {self.insumo.nombre} en {self.reporte}"