from ..dao.reporte_dao import ReporteEmergenciaDAO
from pacientes.models import Paciente
from inventarios.models import InsumoMedico

class ReporteEmergenciaService:

    @staticmethod
    def registrar_reporte(informe, procedimientos, pertenencias, pacientes_ids, insumos_data):
        # Crear el reporte principal
        reporte = ReporteEmergenciaDAO.crear_reporte({
            'informe': informe,
            'procedimientos': procedimientos,
            'pertenencias': pertenencias
        })

        # Asociar pacientes
        for paciente_id in pacientes_ids:
            paciente = Paciente.objects.get(id=paciente_id)
            ReporteEmergenciaDAO.agregar_paciente(reporte, paciente)

        # Asociar insumos
        for item in insumos_data:  # cada item = {'id': insumo_id, 'cantidad': 2}
            insumo = InsumoMedico.objects.get(id=item['id'])
            ReporteEmergenciaDAO.agregar_insumo(reporte, insumo, item['cantidad'])

        return reporte
