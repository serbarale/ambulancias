from ..dao.ambulancia_dao import AmbulanciaDAO

class AmbulanciaService:
    @staticmethod
    def listar_filtradas(estado=None, tipo=None, placa=None):
        return AmbulanciaDAO.filtrar_ambulancias(estado, tipo, placa)

    @staticmethod
    def registrar_ambulancia(datos):
        return AmbulanciaDAO.crear(datos)

    @staticmethod
    def obtener_ambulancia(id):
        return AmbulanciaDAO.obtener_por_id(id)

    @staticmethod
    def actualizar_ambulancia(id, datos):
        instancia = AmbulanciaDAO.obtener_por_id(id)
        return AmbulanciaDAO.actualizar(instancia, datos)
