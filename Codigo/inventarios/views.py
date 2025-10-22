from django.shortcuts import render, redirect, get_object_or_404
from ambulancias.models import Ambulancia
from inventarios.services.checklist_service import CheckListService
from inventarios.services.insumo_service import InsumoService

def submenu_inventarios(request):
    return render(request, 'inventarios/submenu.html')

def buscar_ambulancia_checklist(request):
    placa = request.GET.get('placa')
    ambulancias = Ambulancia.objects.all()

    if placa:
        ambulancias = ambulancias.filter(placa__icontains=placa)

    return render(request, 'inventarios/buscar_ambulancia.html', {
        'ambulancias': ambulancias
    })

def historial_checklist(request, ambulancia_id):
    historial = CheckListService.obtener_historial(ambulancia_id)
    ambulancia = get_object_or_404(Ambulancia, id=ambulancia_id)

    return render(request, 'inventarios/historial.html', {
        'checklists': historial,
        'ambulancia': ambulancia,
    })

def registrar_checklist(request, ambulancia_id):
    ambulancia = get_object_or_404(Ambulancia, id=ambulancia_id)
    insumos = CheckListService.obtener_insumos_por_tipo(ambulancia.tipo_A)

    if request.method == 'POST':
        nombre_colaborador = request.POST.get('nombre_colaborador')
        detalles = []

        for insumo in insumos:
            cantidad = int(request.POST.get(f'insumo_{insumo.id}', 0))
            detalles.append({
                'insumo': insumo,
                'cantidad': cantidad
            })

        datos_checklist = {
            'ambulancia': ambulancia,
            'nombre_colaborador': nombre_colaborador,
        }
        CheckListService.registrar_checklist(datos_checklist, detalles)
        return redirect('historial_checklist', ambulancia_id=ambulancia_id)

    return render(request, 'inventarios/registrar_check.html', {
        'ambulancia': ambulancia,
        'insumos': insumos
    })

def editar_checklist(request, checklist_id):
    # Solo plantilla por ahora, sin lógica
    return render(request, 'inventarios/editar_checklist.html', {
        'checklist_id': checklist_id
    })
    
    
def listar_insumos(request):
    insumos = InsumoService.listar_insumos()
    return render(request, "inventarios/listar_insumo.html", {"insumos": insumos})

def registrar_insumo(request):
    if request.method == 'POST':
        datos = {
            'nombre': request.POST.get('nombre'),
            'stockMinimo': request.POST.get('stockMinimo'),
            'unidadMedida': request.POST.get('unidadMedida'),
            'tipoAmbulancia': request.POST.get('tipoAmbulancia'),
        }
        InsumoService.registrar_insumo(datos)
        return redirect('listar_insumos')

    return render(request, 'inventarios/form_insumo.html', {
        'titulo': 'Registrar Insumo Médico',
        'boton': 'Registrar'
    })

def editar_insumo(request, insumo_id):
    insumo = InsumoService.obtener_insumo(insumo_id)

    if request.method == 'POST':
        datos = {
            'nombre': request.POST.get('nombre'),
            'stockMinimo': request.POST.get('stockMinimo'),
            'unidadMedida': request.POST.get('unidadMedida'),
            'tipoAmbulancia': request.POST.get('tipoAmbulancia'),
        }
        InsumoService.actualizar_insumo(insumo_id, datos)
        return redirect('listar_insumos')

    return render(request, 'inventarios/form_insumo.html', {
        'insumo': insumo,
        'titulo': 'Editar Insumo Médico',
        'boton': 'Actualizar'
    })

def eliminar_insumo(request, insumo_id):
    InsumoService.eliminar_insumo(insumo_id)
    return redirect('listar_insumos')
