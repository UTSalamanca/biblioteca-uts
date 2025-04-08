from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import acervo_model
from .forms import registro_form
from datetime import datetime
from django.contrib import messages
from sito.models import Persona
from sistema.models import UsuarioAcceso, UsuarioManager
from static.helpers import *
from django.utils.timezone import now

# Create your views here.
@groups_required('Administrador')
def index_acervo(request):
    """Devuelve toda la información de acervo hacia el index

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Arreglo con la información filtrada.
    """
    side_code = 200
    listado = acervo_model.objects.all()
    form = registro_form()
    return render(request, 'index_almacen.html', { "list_acervo": listado, "form":form, "side_code":side_code})

@groups_required('Administrador')
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
                return redirect('acervo')
                
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
                    fecharegistro = fecharegistro,
                    fechaedicion = fechaedicion
            )
            messages.add_message(request, messages.SUCCESS, 'Registro agregado')
            return redirect('acervo')
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con errores
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('acervo')
    else:
        form = registro_form()
        messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
        return redirect('acervo')

@groups_required('Administrador')
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
    return redirect(to="acervo")

@groups_required('Administrador')
def edit_register(request, col):
    """Función para filtar y devolver la información de un registro en especifico

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        col (string): Colocación de referencia para el registro 

    Returns:
        array: Retorna arreglo con la información filtrada del registro encontrado
    """
    register = acervo_model.objects.filter(colocacion=col).first()
    listado = acervo_model.objects.all()
    return redirect(reverse('acervo')+'?'+{"register":register})
    # return redirect(request, 'index_almacen.html', { "id_edit": register, "list_acervo": listado})

@groups_required('Administrador')
def edit_acervo(request):
    """Función para realiar la edición de los registros

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        Void
    """
    if request.method == 'POST':
        form = registro_form(request.POST)
        if form.is_valid():
            # Verifica que no exista un duplicado con la misma colocación y formato
            duplicado = acervo_model.objects.filter(
                colocacion=form.cleaned_data['colocacion'], 
                formato=form.cleaned_data['formato']
            ).exclude(id=form.cleaned_data['id'])  # Excluye el actual registro para permitir la actualización
            if duplicado.exists():
                messages.add_message(request, messages.INFO, '¡Ya existe un registro con esa colocación y formato!')
                return redirect('acervo')
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
            return redirect('acervo')
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con errores
            form = registro_form()
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('acervo')
    else:
        form = registro_form()
        messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
        return redirect('acervo')

def temp_formato_add(request):
    ini = 1
    fin = 1641
    format = 'Libro'

    for l in range(ini,fin):
        if l == 1:
            element = acervo_model.objects.filter(id=l).first()
            print(element.formato)
        

    return redirect('inicio')