from django.shortcuts import render, redirect
from .services.historial_service import HistorialService

def submenu(request):
    return render(request, 'pacientes/submenu.html')

def historial_busqueda(request):
    paciente = historial = None
    buscado = False

    if request.method == 'GET':
        dni = request.GET.get('dni')
        nombre = request.GET.get('nombre')
        if dni or nombre:
            paciente, historial = HistorialService.buscar_historial(dni, nombre)
            buscado = True

    return render(request, 'pacientes/historial_busqueda.html', {
        'paciente': paciente,
        'historial': historial,
        'buscado': buscado,
    })

def historial_registrar(request):
    if request.method == 'POST':
        datos_paciente = {
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'dni': request.POST.get('dni'),
            'direccion': request.POST.get('direccion'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
            'fechaNacimiento': request.POST.get('fecha_nacimiento'),
            'sexo': request.POST.get('genero'),  
        }

        datos_historial = {
            'alergias': request.POST.get('alergias'),
            'tipoSangre': request.POST.get('tipo_sangre'),
            'enfermedades': request.POST.get('enfermedades'),
        }

        HistorialService.registrar_historial(datos_paciente, datos_historial)
        return redirect('historial_busqueda')

    return render(request, 'pacientes/historial_form.html', {
        'titulo': 'Registrar Historial Médico',
        'boton': 'Registrar'
    })

def historial_actualizar(request, paciente_id):
    if request.method == 'POST':
        datos_paciente = {
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'dni': request.POST.get('dni'),
            'direccion': request.POST.get('direccion'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
            'fechaNacimiento': request.POST.get('fecha_nacimiento'),
            'sexo': request.POST.get('genero'),
        }

        datos_historial = {
            'alergias': request.POST.get('alergias'),
            'tipoSangre': request.POST.get('tipo_sangre'),
            'enfermedades': request.POST.get('enfermedades'),
        }

        HistorialService.actualizar_historial(paciente_id, datos_paciente, datos_historial)
        return redirect('historial_busqueda')

    paciente, historial = HistorialService.buscar_historial(dni=None, nombre=None)
    return render(request, 'pacientes/historial_form.html', {
        'titulo': 'Actualizar Historial Médico',
        'boton': 'Actualizar',
        'paciente': paciente,
        'historial': historial
    })
