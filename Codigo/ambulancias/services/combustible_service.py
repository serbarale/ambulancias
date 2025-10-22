from ambulancias.dao.combustible_dao import CombustibleDAO
from ambulancias.models import Combustible, Ambulancia
from django.utils.dateparse import parse_date

class CombustibleService:

    @staticmethod
    def obtener_todos():
        return CombustibleDAO.obtener_todos()

    @staticmethod
    def buscar_por_placa(placa):
        return CombustibleDAO.buscar_por_placa(placa)

    @staticmethod
    def filtrar_por_fecha(fecha):
        return CombustibleDAO.filtrar_por_fecha(fecha)

    @staticmethod
    def registrar_combustible(datos):
        ambulancia = Ambulancia.objects.get(id=datos["ambulancia_id"])

        combustible = Combustible(
            fecha_combustible=parse_date(datos["fecha_combustible"]),
            comb_inicial=int(datos["comb_inicial"]),
            comb_final=int(datos["comb_final"]),
            km_inicial=int(datos["km_inicial"]),
            km_final=int(datos["km_final"]),
            nombre_colaborador=datos["nombre_colaborador"],
            ambulancia=ambulancia
        )

        CombustibleDAO.guardar_combustible(combustible)
