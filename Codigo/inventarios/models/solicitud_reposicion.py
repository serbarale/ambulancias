from django.db import models
from inventarios.models import InsumoMedico

class SolicitudReposicion(models.Model):
    insumo = models.ForeignKey(InsumoMedico, on_delete=models.CASCADE)
    cantidad_solicitada = models.IntegerField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aprobada', 'Aprobada'),
            ('rechazada', 'Rechazada')
        ],
        default='pendiente'
    )
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Solicitud {self.id} - {self.insumo.nombre}"