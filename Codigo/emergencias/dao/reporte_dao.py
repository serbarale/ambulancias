from emergencias.models import ReporteEmergencia, ReportePaciente, InsumoUtilizado

class ReporteEmergenciaDAO:
    @staticmethod
    def crear_reporte(data):
        return ReporteEmergencia.objects.create(**data)
    
    @staticmethod
    def agregar_paciente(reporte, paciente):
        return ReportePaciente.objects.create(reporte=reporte, paciente=paciente)
    
    @staticmethod
    def agregar_insumo(reporte, insumo, cantidad):
        return InsumoUtilizado.objects.create(reporte=reporte, insumo=insumo, cantidad=cantidad)
