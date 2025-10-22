from inventarios.models import CheckList, DetalleCheckList

class CheckListDAO:

    @staticmethod
    def crear_checklist(data):
        return CheckList.objects.create(**data)

    @staticmethod
    def listar_por_ambulancia(ambulancia_id):
        return CheckList.objects.filter(ambulancia_id=ambulancia_id).order_by("-fecha_registro")

    @staticmethod
    def obtener_por_id(id):
        return CheckList.objects.get(id=id)


class DetalleCheckListDAO:

    @staticmethod
    def crear_detalles(detalles):
        return DetalleCheckList.objects.bulk_create([
            DetalleCheckList(**detalle) for detalle in detalles
        ])

    @staticmethod
    def obtener_por_checklist(checklist_id):
        return DetalleCheckList.objects.filter(checklist_id=checklist_id)
