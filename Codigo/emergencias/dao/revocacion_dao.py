from ..models import FormatoRevocacion

class FormatoRevocacionDAO:
    @staticmethod
    def crear(datos):
        return FormatoRevocacion.objects.create(**datos)

    @staticmethod
    def obtener_por_informe(informe_id):
        return FormatoRevocacion.objects.filter(informe_id=informe_id).first()
