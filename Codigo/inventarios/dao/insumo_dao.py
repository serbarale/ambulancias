from inventarios.models import InsumoMedico

class InsumoDAO:

    @staticmethod
    def listar():
        return InsumoMedico.objects.all().order_by('nombre')

    @staticmethod
    def obtener_por_id(insumo_id):
        return InsumoMedico.objects.get(id=insumo_id)

    @staticmethod
    def crear(datos):
        return InsumoMedico.objects.create(**datos)

    @staticmethod
    def actualizar(insumo, datos_actualizados):
        for attr, value in datos_actualizados.items():
            setattr(insumo, attr, value)
        insumo.save()
        return insumo

    @staticmethod
    def eliminar(insumo):
        insumo.delete()
