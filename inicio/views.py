from django.shortcuts import render, redirect
from static.utils import dd
from almacen.models import acervo_model
from estadias.models import register_view, model_estadias
from sito.models import Persona, Usuario
from static.helpers import *
from .report_xlsx import generate_report
from catalogo.models import model_catalogo
from datetime import datetime

from collections import Counter
import json

# Create your views here.
def index_inicio(request):
    # Se asigna el código para el focus en el sidebar
    side_code = 100

    if request.user.groups.filter(name='Administrador').exists():
        # Se obtienen todos los datos del acervo
        datos = acervo_model.objects.all()
        # Se realiza el conteo de todos los libros
        totals = cont_books(datos, 't')
        # Se realiza el conteo de los prestamos de libros
        total_prest = cont_books(datos, 'p')
        # Obtener el total por estados
        total_state = get_states(datos)
        # Se realiza el recopilado del tipo de adquisición
        value_adqui = get_adqui(datos)
        """ Registro de vista"""
        ctrl_info = register_view.objects.all()
        ctrl_view = ctrl_view_report(ctrl_info)
        """ fin """

        data = {
            "total_book": totals['total_book'],
            "book_movimiento": total_prest['book_movimiento'],
            "book_prestados_t": total_prest['book_prestados_t'],
            "states": total_state['states'][0],
            "total_state": total_state['total_state'],
            "side_code": side_code,
            "cant_libros":totals['format_libro'],
            "cant_discos": totals['format_disco'],
            "name_cole": value_adqui['name_cole'],
            "value_adqui": value_adqui['value_adqui'],
            "ctrl_view": ctrl_view
        }
        return render(request, 'index_inicio.html', { "data": data })
    else:
        data = {
            "side_code": side_code
        }
        return render(request, 'index_general.html', { "data": data })


def cont_books(datos, type):
    total_book = 0
    totals = {}
    if type == 't':
        format_libro = 0
        format_disco = 0
        for cant in datos:
            if cant.formato == 'book' or cant.formato == 'Libro':
                format_libro += 1
            if cant.formato == 'disc' or cant.formato == 'Disco':
                format_disco += 1
            total_book += cant.cant
        totals = {
            "format_libro": format_libro,
            "format_disco": format_disco,
            "total_book": total_book
        }
    if type == 'p':
        prestamos = model_catalogo.objects.all()
        conteo_m = 0
        conteo_i = 0
        for p in prestamos:
            conteo_m += p.cantidad_m
            conteo_i += p.cantidad_i
            # total_book += 1
        totals = { 
            "book_movimiento": conteo_m,
            "book_prestados_t": conteo_i
        }
    return totals

def get_states(datos):
    states = []
    EXC = 0
    BUE = 0
    REG = 0
    MAL = 0
    for state in datos:
        if state.estado == 'EXC' or state.estado == 'Excelente':
            EXC += 1
        if state.estado == 'BUE' or state.estado == 'Bueno':
            BUE += 1
        if state.estado == 'REG' or state.estado == 'Regular':
            REG += 1
        if state.estado == 'MAL' or state.estado == 'Malo':
            MAL += 1
    # Se almacenan para el uso de al gráfica
    states.append([EXC,BUE,REG,MAL])
    # Suma total de estados (diferente a la suma de todos los libros)
    total_state = states[0][0] + states[0][1] + states[0][2]
    return {
        "states": states,
        "total_state": total_state
    }

def get_adqui(datos):
    t_adqui = []
    name_cole =  []
    for adq in datos:
        ingresa = 'No definido' if adq.adqui == '' else adq.adqui
        t_adqui.append(ingresa)
    # Recorre el arreglo e identifica cuántas veces se repite una elemento
    conteo_adqui = dict(zip(t_adqui, map(lambda x: t_adqui.count(x), t_adqui)))
    value_adqui = []
    for con in conteo_adqui:
        name_cole.append(con)
    for c in range(0, len(name_cole)):
        value_adqui.append(conteo_adqui[name_cole[c]])

    return {
        "value_adqui": value_adqui,
        "name_cole": name_cole
    }

def ctrl_view_report(info):
    data = {}
    data_all = []

    for ctrl in info:
        cve_persona = Usuario.objects.get(login=ctrl.matricula)
        persona = Persona.objects.get(cve_persona=cve_persona.cve_persona)
        data = {
            "fullname": persona.nombre + ' ' + persona.apellido_paterno + ' ' + persona.apellido_materno,
            "persona": ctrl.matricula,
            "reporte": model_estadias.objects.get(id=ctrl.id_reporte).proyecto,
            "carrera": model_estadias.objects.get(id=ctrl.id_reporte).carrera,
            "fecha_consulta": ctrl.fecha_consulta
        }
        data_all.append(data)
    
    return data_all

def format_month(m):
    format = {
        "1": "ENERO",
        "2": "FEBRERO",
        "3": "MARZO",
        "4": "ABRIL",
        "5": "MAYO",
        "6": "JUNIO",
        "7": "JULIO",
        "8": "AGOSTO",
        "9": "SEPTIEMBRE",
        "10": "OCTUBRE",
        "11": "NOVIEMBRE",
        "12": "DICIEMBRE"
    }
    return format[m]

def report(request):
    date = datetime.now()
    year_month = date.strftime('%m %Y')
    cut = year_month.split(' ')
   
    # Obtiene información del acervo
    libros = acervo_model.objects.all()
    # Modelo a comparar, grupos
    modelo_grupo = [
        'ADM', 'MET', 'PIA', 
        'ERC', 'QUIM', 'TIS', 
        'CBA', 'FSC', 'OCL', 
        'OCLEC', 'OCEA', 'OCIG', 
        'FCE', 'IDI', 'LYM',
        'OC', 'Otros'
    ]
    conteo_grupo = {}
    contador = []
    
    for l in libros:
        acortado = l.colocacion.split(" ")
        contador.append(acortado[0])

    conteo = Counter(contador)
    # Crear un diccionario solo con los elementos de modelo_grupo
    cant_for_grp = {grupo: conteo[grupo] for grupo in modelo_grupo}

    data = {
        "ciclo": format_month(cut[0]) + ' ' + cut[1],
        "cant_for_grp": cant_for_grp
    }

    return generate_report(data)