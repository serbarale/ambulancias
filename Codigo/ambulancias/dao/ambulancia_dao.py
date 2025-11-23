from ..models import Ambulancia

class AmbulanciaDAO:
    @staticmethod
    def obtener_todas():
        return Ambulancia.objects.all()

    @staticmethod
    def filtrar_ambulancias(estado=None, tipo=None, placa=None):
        queryset = Ambulancia.objects.all()
        if estado:
            queryset = queryset.filter(estado=estado)
        if tipo:
            queryset = queryset.filter(tipo_A=tipo)
        if placa:
            queryset = queryset.filter(placa__icontains=placa)
        return queryset

    @staticmethod
    def obtener_por_id(id):
        return Ambulancia.objects.get(id=id)

    @staticmethod
    def crear(*args, **kwargs):
        if args and isinstance(args[0], dict):
            datos = args[0]
        else:
            datos = kwargs
        return Ambulancia.objects.create(**datos)

    @staticmethod
    def actualizar(instancia, datos):
        for key, value in datos.items():
            setattr(instancia, key, value)
        instancia.save()
        return instancia
