from ambulancias.models import Avería

class AveriaDAO:
    @staticmethod
    def listar_todas():
        return Avería.objects.all()
    
    @staticmethod
    def buscar_por_placa(placa):
        return Avería.objects.filter(ambulancia__placa__icontains=placa)
    
    @staticmethod
    def filtrar_por_fecha(fecha):
        return Avería.objects.filter(fecha_reporte=fecha)
    
    @staticmethod
    def crear(datos):
        return Avería.objects.create(**datos)
