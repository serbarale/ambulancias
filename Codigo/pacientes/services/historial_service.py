from ..dao.paciente_dao import PacienteDAO
from ..dao.historial_dao import HistorialDAO

class HistorialService:
    @staticmethod
    def buscar_historial(dni=None, nombre=None):
        paciente = PacienteDAO.buscar_por_dni_o_nombre(dni, nombre)
        if paciente:
            historial = HistorialDAO.obtener_por_paciente(paciente)
            return paciente, historial
        return None, None

    @staticmethod
    def registrar_historial(datos_paciente, datos_historial):
        paciente = PacienteDAO.crear_paciente(datos_paciente)
        historial = HistorialDAO.crear_historial(paciente, datos_historial)
        return paciente, historial

    @staticmethod
    def actualizar_historial(paciente_id, datos_paciente, datos_historial):
        from ..models import Paciente
        paciente = Paciente.objects.get(id=paciente_id)
        paciente = PacienteDAO.actualizar_paciente(paciente, datos_paciente)
        historial = HistorialDAO.obtener_por_paciente(paciente)

        if historial:
            historial = HistorialDAO.actualizar_historial(historial, datos_historial)
        else:
            historial = HistorialDAO.crear_historial(paciente, datos_historial)
        return paciente, historial
