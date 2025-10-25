from django.db import models


# Create your models here.
class AmbulanciaManager(models.Manager):
    def create(self, **kwargs):
        # Accept 'tipo' as alias for 'tipo_A' to be compatible with tests
        if 'tipo' in kwargs:
            kwargs['tipo_A'] = kwargs.pop('tipo')
        return super().create(**kwargs)


class Ambulancia(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    ESTADO_AMB = [
        ('preparada', 'Preparada'),
        ('en_proceso', 'En proceso'),
        ('inhabilitada', 'Inhabilitada')]
    estado = models.CharField(max_length=20, choices=ESTADO_AMB, default='en_proceso')
    TIPO_AMB = [
        ('tipo_1', 'Tipo 1'),
        ('tipo_2', 'Tipo 2'),
        ('tipo_3', 'Tipo 3')]
    tipo_A = models.CharField(max_length=10, choices=TIPO_AMB)
    # optional field used by tests; nullable to preserve compatibility
    capacidad = models.IntegerField(null=True, blank=True)
    marca = models.CharField(max_length=50)
    fecha_adquisicion = models.DateField()

    objects = AmbulanciaManager()

    def __str__(self):
        return self.placa
    
class Avería(models.Model):
    TIPO_AVR = [
        ('critico','Crítico'),
        ('grave','Grave'),
        ('leve','Leve')]
    tipoF = models.CharField(max_length=10, choices=TIPO_AVR)
    descripcion_averia = models.TextField()
    ambulancia = models.ForeignKey(Ambulancia, on_delete=models.CASCADE, related_name='averias')
    fecha_reporte = models.DateField(auto_now_add=True)
    nombre_colaborador = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Avería {self.tipoF} en {self.ambulancia.placa} reportado por {self.nombre_colaborador} ({self.fecha_reporte})"
    
class Combustible(models.Model):
    fecha_combustible = models.DateField()
    comb_inicial = models.IntegerField()
    comb_final = models.IntegerField()
    km_inicial = models.IntegerField()
    km_final = models.IntegerField()
    nombre_colaborador = models.CharField(max_length=100)
    ambulancia = models.ForeignKey(Ambulancia, on_delete=models.CASCADE, related_name='combustible')
    
    def __str__(self):
        return f"Combustible de {self.ambulancia.placa} registrado por {self.nombre_colaborador} el {self.fecha_combustible}"

