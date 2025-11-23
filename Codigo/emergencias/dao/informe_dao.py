from emergencias.models import InformeEmergencia

class InformeEmergenciaDAO:
    @staticmethod
    def listar():
        return InformeEmergencia.objects.all().order_by('-fecha_registro')

    @staticmethod
    def buscar_por_placa(placa):
        return InformeEmergencia.objects.filter(ambulancia__placa__icontains=placa).order_by('-fecha_registro')

    @staticmethod
    def filtrar_por_fecha(fecha_inicio, fecha_fin):
        return InformeEmergencia.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    @staticmethod
    def obtener_por_id(id):
        return InformeEmergencia.objects.get(id=id)

    @staticmethod
    def crear(datos):
        datos_modelo = datos.copy()
        if 'direccion_emergencia' in datos_modelo:
            datos_modelo['direccion'] = datos_modelo.pop('direccion_emergencia')
        if 'nombre_paciente' in datos_modelo:
            datos_modelo['paciente_opcional'] = datos_modelo.pop('nombre_paciente')
        
        informe = InformeEmergencia(**datos_modelo)
        informe.full_clean()
        informe.save()
        return informe

    @staticmethod
    def actualizar_estado(id, nuevo_estado):
        informe = InformeEmergencia.objects.get(id=id)
        informe.estado = nuevo_estado
        informe.save()
        return informe
