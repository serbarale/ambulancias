from ambulancias.dao.averia_dao import AveriaDAO
from ambulancias.models import Ambulancia

class AveriaService:
    @staticmethod
    def obtener_todas():
        return AveriaDAO.listar_todas()
    
    @staticmethod
    def buscar_por_placa(placa):
        return AveriaDAO.buscar_por_placa(placa)
    
    @staticmethod
    def filtrar_por_fecha(fecha):
        return AveriaDAO.filtrar_por_fecha(fecha)
    
    @staticmethod
    def registrar_averia(datos):
        # Convertimos el ID en instancia de ambulancia
        ambulancia_id = datos.get("ambulancia")
        if not datos.get("tipoF") or not ambulancia_id:
            raise ValueError("Faltan campos obligatorios.")

        try:
            datos["ambulancia"] = Ambulancia.objects.get(id=ambulancia_id)
        except Ambulancia.DoesNotExist:
            raise ValueError("Ambulancia no encontrada.")

        return AveriaDAO.crear(datos)
