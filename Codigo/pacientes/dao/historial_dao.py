from ..models import HistorialMedico

class HistorialDAO:
    @staticmethod
    def obtener_por_paciente(paciente):
        try:
            return paciente.historial_medico
        except HistorialMedico.DoesNotExist:
            return None

    @staticmethod
    def crear_historial(paciente, datos):
        return HistorialMedico.objects.create(paciente=paciente, **datos)

    @staticmethod
    def actualizar_historial(historial, datos):
        for key, value in datos.items():
            setattr(historial, key, value)
        historial.save()
        return historial
