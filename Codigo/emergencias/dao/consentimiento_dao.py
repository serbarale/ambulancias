from ..models import FormatoConsentimiento

class FormatoConsentimientoDAO:
    @staticmethod
    def crear(datos):
        return FormatoConsentimiento.objects.create(**datos)

    @staticmethod
    def obtener_por_informe(informe_id):
        return FormatoConsentimiento.objects.filter(informe_id=informe_id).first()
