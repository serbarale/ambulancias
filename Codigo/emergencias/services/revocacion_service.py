from ..dao.revocacion_dao import FormatoRevocacionDAO
from emergencias.models import InformeEmergencia

class FormatoRevocacionService:

    @staticmethod
    def generar_formato(informe, datos):
        datos['informe'] = informe
        formato = FormatoRevocacionDAO.crear(datos)
        
        # Cambiar estado del informe a "cancelado"
        informe.estado = 'cancelado'
        informe.save()

        return formato

    @staticmethod
    def obtener_formato(informe):
        return FormatoRevocacionDAO.obtener_por_informe(informe)
