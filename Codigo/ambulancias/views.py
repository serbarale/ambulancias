from django.shortcuts import render, redirect
from django.urls import reverse
from .services.ambulancia_service import AmbulanciaService
from .services.averia_service import AveriaService
from .services.combustible_service import CombustibleService
from .models import Ambulancia, Avería, Combustible
from django.utils.dateparse import parse_date

#CONTROLADORES PARA AMBULANCIAS
def submenu_ambulancias(request):
    return render(request, 'ambulancias/submenu.html')

def listar_ambulancias(request):
    estado = request.GET.get('estado')
    tipo = request.GET.get('tipo')
    placa = request.GET.get('placa')

    ambulancias = AmbulanciaService.listar_filtradas(estado, tipo, placa)

    return render(request, 'ambulancias/listar.html', {
        'ambulancias': ambulancias,
        'estados': Ambulancia.ESTADO_AMB,
        'tipos': Ambulancia.TIPO_AMB,
    })

def registrar_ambulancia(request):
    if request.method == 'POST':
        # Accept both 'tipo' and 'tipo_A' form keys for compatibility
        tipo_val = request.POST.get('tipo_A') or request.POST.get('tipo')
        datos = {
            'placa': request.POST.get('placa'),
            'estado': request.POST.get('estado'),
            'tipo_A': tipo_val,
            'marca': request.POST.get('marca'),
            'fecha_adquisicion': request.POST.get('fecha_adquisicion')
        }
        AmbulanciaService.registrar_ambulancia(datos)
        return redirect(reverse('ambulancias:listar_ambulancias'))
    
    return render(request, 'ambulancias/form.html', {
        'titulo': 'Registrar Ambulancia',
        'boton': 'Registrar',
        'estados': Ambulancia.ESTADO_AMB,
        'tipos': Ambulancia.TIPO_AMB,
    })

def editar_ambulancia(request, id):
    ambulancia = AmbulanciaService.obtener_ambulancia(id)

    if request.method == 'POST':
        tipo_val = request.POST.get('tipo_A') or request.POST.get('tipo')
        datos = {
            'placa': request.POST.get('placa'),
            'estado': request.POST.get('estado'),
            'tipo_A': tipo_val,
            'marca': request.POST.get('marca'),
            'fecha_adquisicion': request.POST.get('fecha_adquisicion')
        }
        AmbulanciaService.actualizar_ambulancia(id, datos)
        return redirect(reverse('ambulancias:listar_ambulancias'))
    
    return render(request, 'ambulancias/form.html', {
        'titulo': 'Editar Ambulancia',
        'boton': 'Actualizar',
        'ambulancia': ambulancia,
        'estados': Ambulancia.ESTADO_AMB,
        'tipos': Ambulancia.TIPO_AMB,
    })

#CONTROLADORES PARA AVERÍAS

def lista_averias(request):
    placa = request.GET.get("placa")
    fecha = request.GET.get("fecha")

    if placa:
        averias = AveriaService.buscar_por_placa(placa)
    elif fecha:
        fecha_parseada = parse_date(fecha)
        averias = AveriaService.filtrar_por_fecha(fecha_parseada)
    else:
        averias = AveriaService.obtener_todas()

    return render(request, "averia/lista_averias.html", {"averias": averias})

# Vista: Registrar avería
def registrar_averia(request):
    ambulancias = Ambulancia.objects.all()

    if request.method == "POST":
        datos = {
            "tipoF": request.POST.get("tipoF"),
            "descripcion_averia": request.POST.get("descripcion_averia"),
            "ambulancia": request.POST.get("ambulancia"),
            "nombre_colaborador": request.POST.get("nombre_colaborador"),
        }
        AveriaService.registrar_averia(datos)
        return redirect(reverse('ambulancias:lista_averias'))

    return render(request, "averia/registrar_averia.html", {"ambulancias": ambulancias})

#CONTROLADORES PARA COMBUSTIBLE

def lista_combustible(request):
    placa = request.GET.get("placa")
    fecha = request.GET.get("fecha")

    if placa:
        registros = CombustibleService.buscar_por_placa(placa)
    elif fecha:
        fecha_parseada = parse_date(fecha)
        registros = CombustibleService.filtrar_por_fecha(fecha_parseada)
    else:
        registros = CombustibleService.obtener_todos()

    return render(request, "combustible/lista_combustible.html", {"registros": registros})

# Vista: Registrar combustible
def registrar_combustible(request):
    ambulancias = Ambulancia.objects.all()

    if request.method == "POST":
        datos = {
            "fecha_combustible": request.POST.get("fecha_combustible"),
            "comb_inicial": request.POST.get("comb_inicial"),
            "comb_final": request.POST.get("comb_final"),
            "km_inicial": request.POST.get("km_inicial"),
            "km_final": request.POST.get("km_final"),
            "nombre_colaborador": request.POST.get("nombre_colaborador"),
            "ambulancia_id": request.POST.get("ambulancia"),
        }
        CombustibleService.registrar_combustible(datos)
        return redirect(reverse('ambulancias:lista_combustible'))

    return render(request, "combustible/registrar_combustible.html", {"ambulancias": ambulancias})