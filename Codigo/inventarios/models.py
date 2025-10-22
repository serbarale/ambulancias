from django.db import models
from ambulancias.models import Ambulancia

# Create your models here.

class InsumoMedico(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    stockMinimo = models.IntegerField(null=False, blank=False)
    UNIDADES =[
        ('unidades', 'Unidades'),
        ('paquetes', 'Paquetes'),
        ('pares', 'Pares'),]
    unidadMedida = models.CharField(max_length=20, choices=UNIDADES, default='unidades', null=False,blank=False)
    
    TIPO_AMBULANCIA = [
        ('tipo_1', 'Tipo 1'),
        ('tipo_2', 'Tipo 2'),
        ('tipo_3', 'Tipo 3')]
    tipoAmbulancia = models.CharField(max_length=10, choices=TIPO_AMBULANCIA, null=False, blank=False)
    
    def __str__(self):
        return self.nombre
    
class CheckList(models.Model):
    ambulancia = models.ForeignKey(Ambulancia, on_delete=models.CASCADE, related_name="checklists")
    nombre_colaborador = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CheckList {self.id} - {self.ambulancia.placa} ({self.fecha_registro.date()})"

class DetalleCheckList(models.Model):
    checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name="detalles")
    insumo = models.ForeignKey(InsumoMedico, on_delete=models.CASCADE)
    cantidad_contada = models.IntegerField()

    def __str__(self):
        return f"{self.insumo.nombre} - {self.cantidad_contada}"
    