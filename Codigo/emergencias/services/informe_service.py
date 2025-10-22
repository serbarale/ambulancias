from ..dao.informe_dao import InformeEmergenciaDAO
from ambulancias.models import Ambulancia
from django.core.exceptions import ValidationError

class InformeEmergenciaService:

    @staticmethod
    def listar_informes():
        return InformeEmergenciaDAO.listar()

    @staticmethod
    def buscar_por_placa(placa):
        return InformeEmergenciaDAO.buscar_por_placa(placa)

    @staticmethod
    def filtrar_por_fecha(fecha_inicio, fecha_fin):
        return InformeEmergenciaDAO.filtrar_por_fecha(fecha_inicio, fecha_fin)

    @staticmethod
    def obtener_por_id(id):
        return InformeEmergenciaDAO.obtener_por_id(id)

    @staticmethod
    def registrar_informe(datos):
        # Validar que exista el ID de ambulancia
        ambulancia_id = datos.get("ambulancia_id")
        if not ambulancia_id:
            raise ValidationError("Debe proporcionar una ambulancia.")

        try:
            ambulancia = Ambulancia.objects.get(id=ambulancia_id)
        except Ambulancia.DoesNotExist:
            raise ValidationError("La ambulancia no existe.")

        # Validar que la ambulancia no esté inhabilitada
        if ambulancia.estado == 'inhabilitada':
            raise ValidationError("No se puede asignar una ambulancia inhabilitada.")

        # Validar campos básicos
        if not datos.get("direccion_emergencia") or not datos.get("nombre_chofer") or not datos.get("prioridad"):
            raise ValidationError("Faltan campos obligatorios para registrar el informe.")

        return InformeEmergenciaDAO.crear(datos)

    @staticmethod
    def actualizar_estado(informe_id, nuevo_estado):
        return InformeEmergenciaDAO.actualizar_estado(informe_id, nuevo_estado)
    
    def obtener_ambulancias_disponibles():
        return Ambulancia.objects.exclude(estado='inhabilitada')
