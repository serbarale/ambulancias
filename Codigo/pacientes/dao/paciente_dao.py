from ..models import Paciente

class PacienteDAO:
    @staticmethod
    def buscar_por_dni_o_nombre(dni=None, nombre=None):
        if dni:
            return Paciente.objects.filter(dni__icontains=dni).first()
        elif nombre:
            return Paciente.objects.filter(nombre__icontains=nombre).first()
        return None

    @staticmethod
    def crear_paciente(datos):
        return Paciente.objects.create(**datos)

    @staticmethod
    def actualizar_paciente(paciente, datos):
        for key, value in datos.items():
            setattr(paciente, key, value)
        paciente.save()
        return paciente
