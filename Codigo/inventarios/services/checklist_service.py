from ..dao.checklist_dao import CheckListDAO, DetalleCheckListDAO
from ambulancias.models import Ambulancia
from inventarios.models import InsumoMedico

class CheckListService:

    @staticmethod
    def registrar_checklist(datos_checklist, detalles_insumos):
        checklist = CheckListDAO.crear_checklist(datos_checklist)
        
        for item in detalles_insumos:
            item["checklist"] = checklist
        DetalleCheckListDAO.crear_detalles(detalles_insumos)

        return checklist

    @staticmethod
    def obtener_historial(ambulancia_id):
        return CheckListDAO.listar_por_ambulancia(ambulancia_id)

    @staticmethod
    def obtener_checklist_con_detalles(id):
        checklist = CheckListDAO.obtener_por_id(id)
        detalles = DetalleCheckListDAO.obtener_por_checklist(id)
        return checklist, detalles

    @staticmethod
    def obtener_insumos_por_tipo(tipo_ambulancia):
        return InsumoMedico.objects.filter(tipoAmbulancia=tipo_ambulancia)

    @staticmethod
    def contar_insumos_a_reponer(insumos):
        return sum(1 for insumo in insumos if insumo["cantidad_contada"] < insumo["stockMinimo"])
