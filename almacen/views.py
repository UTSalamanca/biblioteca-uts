from django.shortcuts import render, redirect
from django.urls import reverse
from .models import acervo_model
from .forms import registro_form
from django.contrib import messages
from static.helpers import *
from django.utils.timezone import now
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
@groups_required('Biblioteca')
def index_acervo(request):
    """Devuelve toda la información de acervo hacia el index

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Arreglo con la información filtrada.
    """
    side_code = 200
    # Acciones para busqueda
    busqueda = request.GET.get("buscar")
    # Obtiene la información del select para filtrar
    m_tab = request.GET.get("m_tab")
    if busqueda:
        all_acervo = acervo_model.objects.filter(
            Q(titulo__icontains = busqueda) |
            Q(autor__icontains = busqueda) |
            Q(editorial__icontains = busqueda) |
            Q(cant__icontains = busqueda) |
            Q(colocacion__icontains = busqueda) |
            Q(edicion__icontains = busqueda) |
            Q(anio__icontains = busqueda) |
            Q(adqui__icontains = busqueda) |
            Q(formato__icontains = busqueda) |
            Q(estado__icontains = busqueda) 
        ).distinct()
    else:
        all_acervo = acervo_model.objects.all()
    # Ordenamiento de datos
    all_acervo = all_acervo.order_by('titulo')
    # Acciones para el paginado
    show_elem = int(m_tab) if m_tab else 10
    paginator = Paginator(all_acervo, show_elem)
    page = request.GET.get('page') or 1
    list_acervo = paginator.get_page(page)
    pagina_actual = int(page)
    total_paginas = list_acervo.paginator.num_pages
    # Definir cuántas páginas mostrar a la vez
    num_mostrar = 5
    mitad = num_mostrar // 2
    # Rango dinámico de páginas a mostrar
    inicio = max(pagina_actual - mitad, 1)
    fin = min(pagina_actual + mitad, total_paginas) +1
    paginas = range(inicio, fin)

    form = registro_form()
    return render(request, 'acervo/index_almacen.html', { 
        "list_acervo": list_acervo, 
        "paginas":paginas, 
        "pagina_actual":pagina_actual, 
        "form":form, 
        "side_code":side_code })

@groups_required('Biblioteca')
def get_match(request):
    """Función para la busqueda de coincidencias en actualiación de registros

    Args:
        request (object): objeto de HTTP

    Returns:
        integer: 0 => Sin coincidencia, 1 => Coincidencia
    """
    try:
        acervo_exist = acervo_model.objects.filter(
            colocacion=request.GET['col'], 
            formato=request.GET['format']
            ).exclude(id=request.GET['id'])  # Excluye el actual registro para permitir la actualización
        respuesta = 0
        if acervo_exist.exists():
            respuesta = 1
        return JsonResponse({'respuesta': respuesta})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@groups_required('Biblioteca')
def get_register(request):
    """Función para la busqueda de coincidencias para nuevos registro en acervo

    Args:
        request (object): objeto de HTTP

    Returns:
        integer: 0 => Sin coincidencia, 1 => Coincidencia
    """
    try:
        acervo_exist = acervo_model.objects.filter(
            colocacion=request.GET['col'], 
            formato=request.GET['format']
            )
        respuesta = 0
        if acervo_exist.exists():
            respuesta = 1
        return JsonResponse({'respuesta': respuesta})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@groups_required('Biblioteca')
def acervo_registro(request):
    """Función para agregar un nuevo registro en base de datos

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        Void
    """
    if request.method == 'POST':
        form = registro_form(request.POST)
        if form.is_valid():
            # Valida que la colocación no sea repetida
            acervo_exist = acervo_model.objects.filter(colocacion=form.cleaned_data['colocacion'], formato=form.cleaned_data['formato'])
            if acervo_exist.exists():
                messages.add_message(request, messages.INFO, 'Ya existe un elemento con esta colocación')
                return redirect('acervo:acervo')
                
            titulo = form.cleaned_data['titulo']
            autor = form.cleaned_data['autor']
            editorial = form.cleaned_data['editorial']
            cant = form.cleaned_data['cant']
            colocacion = form.cleaned_data['colocacion']
            edicion = form.cleaned_data['edicion']
            anio = form.cleaned_data['anio']
            adqui = form.cleaned_data['adqui']
            formato = form.cleaned_data['formato']
            estado = form.cleaned_data['estado']
            base64 = ""
            fecharegistro = now().replace(microsecond=0)
            fechaedicion = now().replace(microsecond=0)
            
            acervo = acervo_model.objects.create(
                    titulo = titulo,
                    autor = autor,
                    editorial = editorial,
                    cant = cant,
                    colocacion = colocacion,
                    edicion = edicion,
                    anio = anio,
                    adqui = adqui,
                    formato = formato,
                    estado = estado,
                    base64 = base64,
                    fecharegistro = fecharegistro,
                    fechaedicion = fechaedicion
            )
            print(acervo)
            messages.add_message(request, messages.SUCCESS, 'Registro agregado')
            return redirect('acervo:acervo')
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con errores
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('acervo:acervo')
    else:
        form = registro_form()
        messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
        return redirect('acervo:acervo')

@groups_required('Biblioteca')
def delete_acervo(request, col):
    """Función para el borrado de registros de base de datos

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        col (string): Colocación de referencia del registro

    Returns:
        Void
    """
    acervo_delete = acervo_model.objects.filter(colocacion=col).first()
    acervo_delete.delete()
    messages.add_message(request, messages.SUCCESS, 'Registro eliminado')
    return redirect(to="acervo:acervo")

@groups_required('Biblioteca')
def edit_register(request, col):
    """Función para filtar y devolver la información de un registro en especifico

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        col (string): Colocación de referencia para el registro 

    Returns:
        array: Retorna arreglo con la información filtrada del registro encontrado
    """
    register = acervo_model.objects.filter(colocacion=col).first()
    return redirect(reverse('acervo:acervo')+'?'+{"register":register})

@groups_required('Biblioteca')
def edit_acervo(request):
    """Función para realiar la edición de los registros

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        Void
    """
    if request.method == 'POST':
        form = registro_form(request.POST)
        print('llega edit_acervo')
        if form.is_valid():
            print(form.cleaned_data['id'])
            # Verifica que no exista un duplicado con la misma colocación y formato
            duplicado = acervo_model.objects.filter(
                colocacion=form.cleaned_data['colocacion'], 
                formato=form.cleaned_data['formato']
            ).exclude(id=form.cleaned_data['id'])  # Excluye el actual registro para permitir la actualización
            if duplicado.exists():
                messages.add_message(request, messages.INFO, '¡Ya existe un registro con esa colocación y formato!')
                return redirect('acervo:acervo')
            element = acervo_model.objects.get(id=form.cleaned_data['id'])
            element.titulo = form.cleaned_data['titulo']
            element.autor = form.cleaned_data['autor'] if request.POST.get('autor') else ''
            element.editorial = form.cleaned_data['editorial'] if request.POST.get('editorial') else ''
            element.cant = form.cleaned_data['cant']
            element.colocacion = form.cleaned_data['colocacion']
            element.edicion = form.cleaned_data['edicion'] if request.POST.get('edicion') else ''
            element.anio = form.cleaned_data['anio']  if request.POST.get('anio') else ''
            element.adqui = form.cleaned_data['adqui']  if request.POST.get('adqui') else ''
            element.estado = form.cleaned_data['estado']
            element.formato = form.cleaned_data['formato']
            element.fechaedicion = now().replace(microsecond=0)
            element.save()
            # Muestra un mensaje de éxito si no existe un problema
            # Retorna hacia Acervo
            messages.add_message(request, messages.SUCCESS, 'Registro actualizado')
            return redirect('acervo:acervo')
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con errores
            form = registro_form()
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('acervo:acervo')
    else:
        form = registro_form()
        messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
        return redirect('acervo:acervo')

def temp_formato_add(request):
    ini = 1
    fin = 1641
    format = 'Libro'

    for l in range(ini,fin):
        if l == 1:
            element = acervo_model.objects.filter(id=l).first()
            print(element.formato)
        

    return redirect('inicio:inicio')