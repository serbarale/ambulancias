from ambulancias.models import Combustible

class CombustibleDAO:

    @staticmethod
    def obtener_todos():
        return Combustible.objects.all().order_by('-fecha_combustible')

    @staticmethod
    def buscar_por_placa(placa):
        return Combustible.objects.filter(ambulancia__placa__icontains=placa).order_by('-fecha_combustible')

    @staticmethod
    def filtrar_por_fecha(fecha):
        return Combustible.objects.filter(fecha_combustible=fecha).order_by('-fecha_combustible')

    @staticmethod
    def guardar_combustible(combustible):
        combustible.save()
