from django.shortcuts import render, redirect
from .models import model_estadias, register_view
from .forms import estadias_form
import os
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from static.helpers import *
from django.contrib import messages
from static.utils import dd
from sito.models import Alumno, AlumnoGrupo, Grupo, Carrera, Usuario, Persona, Periodo
from static.context_processors import group_permission
from django.http import JsonResponse
import base64
import tempfile
import time
from django.utils.timezone import localtime
from django.utils.timezone import now

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def add_group_name_to_contex(view_class):
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        print(user)

# Función que obtiene todos los grupos de control y el nombre del usuario registrado
def get_fullname_grupo(request):
    user = request.user
    cve = Usuario.objects.get(login=user)
    persona = Persona.objects.get(cve_persona=cve.cve_persona)
    group = group_permission(request, True)
    name = persona.nombre + ' ' + persona.apellido_paterno + ' ' + persona.apellido_materno
    return {
        "group": group['grupo_control'],
        "name": name
    }

# Index principal
def index_proyectos(request):
    form = estadias_form()
    # Código para control de pestañas en sidebar
    side_code = 300
    # fullname = get_fullname_grupo(request)['name']
    # flag = True
    # if '32 Tutoreo - Tutor' in get_fullname_grupo(request)['group']:
    #     flag = False
    #     reporte = model_estadias.objects.filter(asesor_academico=fullname)
    #     reporte_all = model_estadias.objects.all()
    #     return render(request,'index_proyectos.html',{"reporte":reporte, "reporte_all":reporte_all, "form":form,"side_code":side_code})
    
    reporte = model_estadias.objects.all()
    return render(request,'index_proyectos.html',{"reporte":reporte, "form":form,"side_code":side_code})

@groups_required('32 Tutoreo - Tutor', 'Administrador')
def estadias_registro(request):
    try:
        if request.method == 'POST':
            # Validar existencia de proyectos
            exist_proyect = model_estadias.objects.filter(
                matricula=request.POST['matricula'], 
                proyecto=request.POST['proyecto'], 
                generacion=request.POST['generacion']
            )
            if exist_proyect:
                messages.add_message(request, messages.INFO, 'Este proyecto ya fue registrado con el mismo alumno')
                return redirect('proyectos')

            exist_name_proyect = model_estadias.objects.filter(proyecto=request.POST['proyecto'])
            if exist_name_proyect:
                messages.add_message(request, messages.INFO, 'Ya existe un proyecto con este nombre')
                return redirect('proyectos')

            # Validar archivo antes de procesarlo
            if not request.FILES['reporte_file']:
                messages.add_message(request, messages.ERROR, 'Debe subir un archivo válido.')
                return redirect('proyectos')
            
            form = estadias_form(request.POST, request.FILES)
            if form.is_valid():
                # Datos validados desde el formulario
                matricula = form.cleaned_data['matricula']
                proyecto = form.cleaned_data['proyecto']
                generacion = form.cleaned_data['generacion']
                alumno = form.cleaned_data['alumno']
                asesor_academico = form.cleaned_data['asesor_academico']
                empresa = form.cleaned_data['empresa']
                asesor_orga = form.cleaned_data['asesor_orga']
                carrera = form.cleaned_data['carrera']
                archivo = form.cleaned_data['reporte_file']
                # Procesar archivo y datos
                name_ref = file_new_name(alumno, archivo.name)
                base64_file = convert_base64(archivo)
                fecha_registro = now().replace(microsecond=0)

                # Crear registro
                model_estadias.objects.create(
                    proyecto=proyecto,
                    matricula=matricula,
                    alumno=alumno,
                    asesor_academico=asesor_academico,
                    generacion=generacion,
                    empresa=empresa,
                    asesor_orga=asesor_orga,
                    carrera=carrera,
                    reporte=name_ref,
                    base64=base64_file,
                    fecha_registro=fecha_registro
                )
                messages.add_message(request, messages.SUCCESS, 'Registro agregado correctamente')
                return redirect('proyectos')
            else:
                # Mostrar errores del formulario
                print(form.errors)
                messages.add_message(request, messages.ERROR, 'Por favor, corrija los errores en el formulario')
        else:
            form = estadias_form()

        return render(request, 'index_proyectos.html', {'form': form})
    except AttributeError as e:
        print(f"Error específico: {e}")
        return HttpResponse("Error relacionado con atributos de archivo.", status=400)
    except Exception as re:
        print(f"Algo salió mal: {re}")
        return HttpResponse("Ocurrió un error inesperado.", status=500)

# Función para convertir documento a base64
def convert_base64(file):
    try:
        if not hasattr(file, 'read'):
            raise ValueError("El archivo no es válido o no tiene datos para leer.")
        return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error al convertir archivo a base64: {e}")
        return None

# Crea el archivo temporal para la visualización del mismo
def temporary_file_base_64(base_64_input):
    # base64_string = base_64_input.strip().split(',')[1]
    decoded_bytes = base64.b64decode(base_64_input)
    file_temp, path_temp = tempfile.mkstemp(suffix=".pdf", dir=settings.MEDIA_ROOT + "/")
    try:
        with os.fdopen(file_temp, 'wb') as tmp:
            tmp.write(decoded_bytes)
    except Exception as e:
        os.remove(path_temp)
        raise e
    return path_temp

# Función para mostrar file report
def view_report(request, report_rute):
    try:
        # Código de ubicación para sidebar
        side_code = 301
        id_reporte = model_estadias.objects.filter(reporte=report_rute).first()
        # Se crea el archivo temporal y se obtiene la ruta
        name_temp = temporary_file_base_64(id_reporte.base64)
        # Se separan los datos no necesarios
        ruta = name_temp.split('/code')[1]

        return render(request, 'iframe_pdf.html', {'reporte': ruta, "side_code":side_code, "alumno":id_reporte})
    except Exception as v:
        print(f"Error en al generar vista de PDF: {v}")

def insert_consult(request):
    try:
        user_id = request.POST.get('user_id')
        name_reporte = request.POST.get('name_reporte')
        ref_reporte = request.POST.get('id_reporte')

        if request.method == 'POST':
            id_reporte = ref_reporte
            matricula = user_id
            consultas = 1
            fecha_consulta = now().replace(microsecond=0)

            register_view.objects.create(
                id_reporte = id_reporte,
                matricula = matricula,
                consultas = consultas,
                fecha_consulta = fecha_consulta
            )
        data = {
            "success": True,
            "message": "Registro actualizado exitosamente.",
            "name_reporte": name_reporte,
            "consultas": consultas,
            "fecha_consulta": fecha_consulta.strftime("%d/%m/%Y"),
        }

        return JsonResponse(data)

    except register_view.DoesNotExist:
        return JsonResponse({"success": False, "message": "El registro no existe."}, status=404)

    except Exception as a:
        # Imprime el error para depuración y devuelve una respuesta de error
        print(f"Algo salió mal: {a}")
        return JsonResponse({"success": False, "message": "Error al procesar la solicitud."}, status=500)

def servir_pdf(request, report_rute):
    file_path = os.path.join(settings.MEDIA_ROOT, report_rute)
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mi_documento.pdf"'
    return response

@groups_required('32 Tutoreo - Tutor', 'Administrador')
# Función de búsqueda para retorno de información por búsqueda con matricula
def get_alumno(request):
    matricula = request.GET.get('matricula')
    if matricula:
        cve_persona = ''
        try:
            # alumno_grupo = get_object_or_404(AlumnoGrupo, matricula=matricula)
            alumno_grupo = AlumnoGrupo.objects.filter(matricula=matricula).values_list('cve_grupo', flat=True)
            cve_grupo = alumno_grupo[len(alumno_grupo) - 1]
            grupo = Grupo.objects.get(cve_grupo=cve_grupo)
            carrera = Carrera.objects.get(nombre=grupo.cve_carrera)
            generacion = Alumno.objects.get(matricula=matricula)
            cve_persona = Usuario.objects.get(login=matricula)
            persona = Persona.objects.get(cve_persona=cve_persona.cve_persona)
            data = {
                "nombre": persona.nombre,
                "apellido_paterno": persona.apellido_paterno,
                "apellido_materno": persona.apellido_materno,
                "nombre_grupo": grupo.nombre,
                "nombre_carrera": carrera.nombre,
                "generacion": generacion.generacion
            }
            return JsonResponse(data)
        except Exception as a:
            print(f"Algo salio mal: {a}")
    return JsonResponse({'error': 'Matricula no proporcionada'}, status=400)
