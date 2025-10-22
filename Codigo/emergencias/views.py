from django.shortcuts import render, redirect, get_object_or_404
from emergencias.models import InformeEmergencia
from django.contrib import messages
from emergencias.services.informe_service import InformeEmergenciaService
from emergencias.services.reporte_service import ReporteEmergenciaService
from .services.consentimiento_service import FormatoConsentimientoService
from .services.revocacion_service import FormatoRevocacionService
from pacientes.models import Paciente
from inventarios.models import InsumoMedico
from ambulancias.models import Ambulancia

def listar_informes_emergencia(request):
    informes = InformeEmergencia.objects.all().order_by("-fecha_registro")

    # Filtros
    prioridad = request.GET.get("prioridad")
    placa = request.GET.get("placa")

    if prioridad:
        informes = informes.filter(prioridad=prioridad)

    if placa:
        informes = informes.filter(ambulancia__placa__icontains=placa)

    return render(request, "emergencias/listar_informes.html", {
        "informes": informes,
        "prioridades": InformeEmergencia.PRIORIDADES,  
        "filtro_actual": {
            "prioridad": prioridad or "",
            "placa": placa or ""
        },
        "origen": "ambulancias"
    })
    
def asignar_ambulancia(request):
    placa = request.GET.get("placa")
    estado = request.GET.get("estado")
    tipo = request.GET.get("tipo")
    ambulancias = InformeEmergenciaService.obtener_ambulancias_disponibles()

    if placa:
        ambulancias = ambulancias.filter(placa__icontains=placa)
    if estado:
        ambulancias = ambulancias.filter(estado=estado)
    if tipo:
        ambulancias = ambulancias.filter(tipo_A=tipo)

    context = {
        "ambulancias": ambulancias,
        "estados": Ambulancia.ESTADO_AMB,
        "tipos": Ambulancia.TIPO_AMB,
    }
    return render(request, "emergencias/asignar_ambulancia.html", context)

def registrar_informe(request, ambulancia_id):  # ← Agregado ambulancia_id
    # Obtener la ambulancia específica que se seleccionó
    try:
        ambulancia = Ambulancia.objects.get(id=ambulancia_id)
    except Ambulancia.DoesNotExist:
        messages.error(request, "Ambulancia no encontrada.")
        return redirect("asignar_ambulancia")

    # Obtener las opciones de prioridad para el formulario
    prioridades = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]  # Ajusta según tus choices del modelo

    if request.method == "POST":
        datos = {
            "ambulancia_id": ambulancia_id,  # Usar el ID de la URL
            "direccion_emergencia": request.POST.get("direccion_emergencia"),
            "nombre_chofer": request.POST.get("nombre_chofer"),
            "prioridad": request.POST.get("prioridad"),
            "nombre_paciente": request.POST.get("nombre_paciente")  # opcional
        }

        try:
            InformeEmergenciaService.registrar_informe(datos)
            messages.success(request, "Informe registrado correctamente.")
            return redirect("lista_informes_emergencia")
        except Exception as e:
            messages.error(request, f"Error al registrar informe: {str(e)}")

    return render(request, "emergencias/registrar_informe.html", {
        "ambulancia": ambulancia,  # Pasar la ambulancia específica
        "prioridades": prioridades,
    })
    
def listar_informes_desde_pacientes(request):
    informes = InformeEmergencia.objects.all().order_by("-fecha_registro")

    # Filtros 
    prioridad = request.GET.get("prioridad")
    placa = request.GET.get("placa")

    if prioridad:
        informes = informes.filter(prioridad=prioridad)

    if placa:
        informes = informes.filter(ambulancia__placa__icontains=placa)

    return render(request, "emergencias/listar_informes.html", {
        "informes": informes,
        "prioridades": InformeEmergencia.PRIORIDADES,  
        "filtro_actual": {
            "prioridad": prioridad or "",
            "placa": placa or ""
        },
        "origen": "pacientes"  
    })

def detalles_informe(request, informe_id):
    informe = get_object_or_404(InformeEmergencia, id=informe_id)
    return render(request, "emergencias/detalles_informe.html", {"informe": informe})

def generar_revocacion(request, id):
    informe = get_object_or_404(InformeEmergencia, id=id)

    if request.method == 'POST':
        datos = {
            'nombre_declarante': request.POST.get('nombre_declarante'),
            'tipo_persona': request.POST.get('tipo_persona'),
            'tipo_documento': request.POST.get('tipo_documento'),
            'numero_documento': request.POST.get('numero_documento'),
            'motivo_revocacion': request.POST.get('motivo_revocacion'),
            'nombre_testigo': request.POST.get('nombre_testigo'),
        }

        FormatoRevocacionService.generar_formato(informe, datos)
        return redirect('detalles_informe', informe_id=informe.id)

    return render(request, 'emergencias/revocacion.html', {'informe': informe})

# Generar formato de consentimiento

def generar_consentimiento(request, id):
    informe = get_object_or_404(InformeEmergencia, id=id)

    if request.method == "POST":
        datos = {
            "informe": informe,
            "lugar": request.POST.get("lugar"),
            "nombre_paciente": request.POST.get("nombre_paciente"),
            "dni_paciente": request.POST.get("dni_paciente"),
            "personal_medico": request.POST.get("personal_medico"),
            "acepta_acto_medico": bool(request.POST.get("acto_medico")),
            "acepta_traslado": bool(request.POST.get("traslado")),
        }
        FormatoConsentimientoService.registrar_consentimiento(datos)
        return redirect("detalles_informe", informe_id=informe.id)

    return render(request, "emergencias/consentimiento.html", {"informe": informe})

# Generar reporte de emergencia asistida
def generar_reporte_emergencia(request, id):
    informe = get_object_or_404(InformeEmergencia, id=id)

    if request.method == "POST":
        procedimientos = request.POST.get("procedimientos")
        pertenencias = request.POST.get("pertenencias")

        # IDs de pacientes seleccionados
        pacientes_ids = request.POST.getlist("pacientes")  # ['1', '2', ...]

        # Insumos seleccionados (en formato: insumo_id|cantidad)
        insumos_raw = request.POST.getlist("insumos")  # ['3|2', '5|1']
        insumos_data = []
        for item in insumos_raw:
            insumo_id, cantidad = item.split('|')
            insumos_data.append({'id': int(insumo_id), 'cantidad': int(cantidad)})

        # Guardar reporte con sus relaciones
        ReporteEmergenciaService.registrar_reporte(
            informe, procedimientos, pertenencias, pacientes_ids, insumos_data
        )

        return redirect("detalles_informe", informe_id=informe.id)

    # Datos para buscar en el formulario
    pacientes = Paciente.objects.all()
    insumos = InsumoMedico.objects.all()

    return render(request, "emergencias/reporte_emergencia.html", {
        "informe": informe,
        "pacientes": pacientes,
        "insumos": insumos,
    })
