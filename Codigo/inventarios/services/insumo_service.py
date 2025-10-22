from inventarios.dao.insumo_dao import InsumoDAO
from django.shortcuts import get_object_or_404

class InsumoService:

    @staticmethod
    def listar_insumos():
        return InsumoDAO.listar()

    @staticmethod
    def obtener_insumo(insumo_id):
        return get_object_or_404(InsumoDAO.listar(), id=insumo_id)

    @staticmethod
    def registrar_insumo(datos):
        return InsumoDAO.crear(datos)

    @staticmethod
    def actualizar_insumo(insumo_id, datos):
        insumo = InsumoDAO.obtener_por_id(insumo_id)
        return InsumoDAO.actualizar(insumo, datos)

    @staticmethod
    def eliminar_insumo(insumo_id):
        insumo = InsumoDAO.obtener_por_id(insumo_id)
        InsumoDAO.eliminar(insumo)
