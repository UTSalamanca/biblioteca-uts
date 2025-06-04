from django.shortcuts import render
from almacen.models import acervo_model
from estadias.models import register_view, model_estadias
from sito.models import Persona, Usuario, Carrera
from static.helpers import *
from .report_xlsx import generate_report
from catalogo.models import model_catalogo
from datetime import datetime, timedelta
import calendar
from django.core.paginator import Paginator
from django.db.models import Q, Sum

# Create your views here.
def index_inicio(request):
    """Devuelve información formateada para muestra en el index segun el tipo de perfil

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Información recopilada
    """
    # Se asigna el código para el focus en el sidebar
    side_code = 100
    if request.user.groups.filter(name='Biblioteca').exists():
        
        total_books_cant = acervo_model.objects.all().aggregate(Sum('cant'))['cant__sum']
        # Get total borrowed books in the current month
        now = datetime.now()
        year = now.year
        month = now.month
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year, month, 31)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        total_borrowed_books = model_catalogo.objects.filter(
            fechaP__gte=first_day, fechaP__lte=last_day
        ).aggregate(Sum('cantidad_i'))['cantidad_i__sum']
        print(total_books_cant, total_borrowed_books)

        context = {
            "side_code": side_code,
            "total_books_cant": total_books_cant,
            "total_borrowed_books": total_borrowed_books
        }

        
        return render(request, 'inicio/index_inicio.html', context)
    else:
        context = {
            "side_code": side_code
        }
        return render(request, 'inicio/index_general.html', context)

def cont_books(datos, type):
    """Contreo de ejemplares

    Args:
        datos (array): Información obtenida de la tabla
        type (string): Tipo de consulta

    Returns:
        array: Información formateada
    """
    total_book = 0
    totals = {}
    if type == 't':
        format_libro = 0
        format_disco = 0
        format_revista = 0
        for cant in datos:
            if cant.formato == 'book' or cant.formato == 'Libro':
                format_libro += 1
            if cant.formato == 'disc' or cant.formato == 'Disco':
                format_disco += 1
            if cant.formato == 'Revista':
                format_revista += 1
            total_book += cant.cant
        totals = {
            "format_libro": format_libro,
            "format_disco": format_disco,
            "format_revista": format_revista,
            "total_book": total_book
        }
    if type == 'p':
        prestamos = model_catalogo.objects.all()
        date = datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        # Define mes de consulta
        _, num_days = calendar.monthrange(int(year), int(month))
        fech_ini = f"{year}-{month}-01"
        fech_fin = f"{year}-{month}-{num_days}"
        conteo_m = 0
        conteo_i = 0
        for p in prestamos:
            conteo_m += p.cantidad_m
            expl = str(p.fechaP).split(' ')
            # print(expl[0])
            if expl[0] >= fech_ini and expl[0] <= fech_fin:
                conteo_i += p.cantidad_i
            # total_book += 1
        totals = { 
            "book_movimiento": conteo_m,
            "book_prestados_t": conteo_i
        }
    return totals

def get_states(datos):
    """Realiza el conteo de los estados

    Args:
        datos (array): Información completa de los estados

    Returns:
        array: Información formateada
    """
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
    """Realiza el conteo de los tipos de adquisiciones

    Args:
        datos (array): Información completa de las aquisiciones 

    Returns:
        array: Información formateada
    """
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
    """Recopila la vistas realizadas a los reportes

    Args:
        info (array): información de todas las vistas

    Returns:
        array: información formateada
    """
    data = {}
    data_all = []
    # Obtiene el periodo de consulta
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

def get_periodo(periodo):
    """Se obtiene el ciclo y el rango de fechas para consulta en filtro de periodo

    Args:
        periodo (integer): Bandera para indicar el mes a consultar 
        1 = mes actual
        2 = mes anterior

    Returns:
        array: Retorna arreglo
        - Fecha inicial
        - Fecha final
        - Ciclo
    """
    format = {
        "01": "ENERO",
        "02": "FEBRERO",
        "03": "MARZO",
        "04": "ABRIL",
        "05": "MAYO",
        "06": "JUNIO",
        "07": "JULIO",
        "08": "AGOSTO",
        "09": "SEPTIEMBRE",
        "10": "OCTUBRE",
        "11": "NOVIEMBRE",
        "12": "DICIEMBRE"
    }
    date = datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    # Define mes de consulta
    calc = int(month) - int(periodo)
    _, num_days = calendar.monthrange(int(year), int(calc))

    calc_mes = f"0{calc}" if len(str(calc)) == 1 else calc

    if len(str(calc)) == 1:
        ciclo = format[f"0{calc}"]
    else:
        ciclo = format[calc]

    data = {
        'fech_ini': f"{year}-{calc_mes}-01",
        'fech_fin': f"{year}-{calc_mes}-{num_days}",
        'ciclo': ciclo
    }

    return data

def periodo_consulta(periodo):
    """Se obtiene el ciclo y el rango de fechas para consulta

    Args:
        periodo (integer): Bandera para indicar el mes a consultar 
        1 = mes actual
        2 = mes anterior

    Returns:
        array: Retorna arreglo
        - Fecha inicial
        - Fecha final
        - Ciclo
    """
    # Arreglo para obtención nombre de mes
    format = {
        "01": "ENERO",
        "02": "FEBRERO",
        "03": "MARZO",
        "04": "ABRIL",
        "05": "MAYO",
        "06": "JUNIO",
        "07": "JULIO",
        "08": "AGOSTO",
        "09": "SEPTIEMBRE",
        "10": "OCTUBRE",
        "11": "NOVIEMBRE",
        "12": "DICIEMBRE"
    }
    date = datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    # Define mes de consulta
    # resta = 1 if periodo == 1 else 0
    calc = int(month) - periodo
    _, num_days = calendar.monthrange(int(year), int(calc))

    calc_mes = f"0{calc}" if len(str(calc)) == 1 else calc

    if len(str(calc)) == 1:
        ciclo = format[f"0{calc}"]
    else:
        ciclo = format[calc]

    return {
        'fech_ini': f"{year}-{calc_mes}-01",
        'fech_fin': f"{year}-{calc_mes}-{num_days}",
        'ciclo': ciclo
    }

def report(request, periodo):
    """Recopila datos para la generación del reporte mensual

    Args:
        request (object): Información sobre la solicitud HTTP entrante
        periodo (integer): Bandera para indicar el mes a consultar 
        1 = mes actual
        2 = mes anterior

    Returns:
        instancia: Retorna instancia de la creación del reporte, para que pueda ser descargado.
    """
    dato_periodo = periodo_consulta(periodo)
    fech_ini = dato_periodo['fech_ini']
    fech_fin = dato_periodo['fech_fin']
    ciclo = dato_periodo['ciclo']
    # Obtiene información del acervo
    libros = acervo_model.objects.all()
    cantidad_libro = {}
    volumen_libro = {}
    cantidad_disco = {}
    volumen_disco = {}
    volumen_revista = {}
    cantidad_revista = {}
    conteo_ejemplares = []
    for libro in libros:
        formato = libro.formato
        acortado = libro.colocacion.split(" ")
        ejemplar = acortado[0]
        # Recopila las abreviaciones de las colocación
        conteo_ejemplares.append(ejemplar) if ejemplar not in conteo_ejemplares else ''
        # Calcula los voluemes de los ejemplares
        # Calcula la cantidad de ejemplares
        if formato == 'Libro':
            if len(volumen_libro) != 0:
                if ejemplar in volumen_libro:
                    volumen_libro[ejemplar] = volumen_libro[ejemplar] + libro.cant
                    cantidad_libro[ejemplar] = cantidad_libro[ejemplar] + 1
                else:
                    volumen_libro[ejemplar] = libro.cant
                    cantidad_libro[ejemplar] = 1
            else:
                volumen_libro[ejemplar] = libro.cant
                cantidad_libro[ejemplar] = 1
        if formato == 'Disco':
            if len(volumen_disco) != 0:
                if ejemplar in volumen_disco:
                    volumen_disco[ejemplar] = volumen_disco[ejemplar] + libro.cant
                    cantidad_disco[ejemplar] = cantidad_disco[ejemplar] + 1
                else:
                    volumen_disco[ejemplar] = libro.cant
                    cantidad_disco[ejemplar] = 1
            else:
                volumen_disco[ejemplar] = libro.cant
                cantidad_disco[ejemplar] = 1
        if formato == 'Revista':
            if len(volumen_revista) != 0:
                if ejemplar in volumen_revista:
                    volumen_revista[ejemplar] = volumen_revista[ejemplar] + libro.cant
                    cantidad_revista[ejemplar] = cantidad_revista[ejemplar] + 1
                else:
                    volumen_revista[ejemplar] = libro.cant
                    cantidad_revista[ejemplar] = 1
            else:
                volumen_revista[ejemplar] = libro.cant
                cantidad_revista[ejemplar] = 1
    # Obtiene todas las carreras activas
    carreras = Carrera.objects.all()
    conc_adquisicion = {}
    conc_adquisicion['fecha_inicial'] = fech_ini
    conc_adquisicion['fecha_final'] = fech_fin
    adquisiciones = {}
    adqui_vol_libro = {}
    adqui_cant_libro = {}
    adqui_vol_disco = {}
    adqui_cant_disco = {}
    adqui_vol_revista = {}
    adqui_cant_revista = {}
    for carrera in conteo_ejemplares:
        for libro in libros:
            if str(libro.fecharegistro) >= fech_ini and str(libro.fecharegistro) <= fech_fin:
                # Existe coincidencia con la carrer y la colocación
                if carrera in libro.colocacion:
                    # Se separa por formato
                    if libro.formato == 'Libro':
                        if carrera in adqui_cant_libro:
                            adqui_vol_libro[carrera] = adqui_vol_libro[carrera] + libro.cant
                            adqui_cant_libro[carrera] = adqui_cant_libro[carrera] + 1
                        else: 
                            adqui_vol_libro[carrera] = libro.cant
                            adqui_cant_libro[carrera] = 1
                    if libro.formato == 'Disco':
                        if carrera in adqui_cant_disco:
                            adqui_vol_disco[carrera] = adqui_vol_disco[carrera] + libro.cant
                            adqui_cant_disco[carrera] = adqui_cant_disco[carrera] + 1
                        else: 
                            adqui_vol_disco[carrera] = libro.cant
                            adqui_cant_disco[carrera] = 1
                    if libro.formato == 'Revista':
                        if carrera in adqui_cant_revista:
                            adqui_vol_revista[carrera] = adqui_vol_revista[carrera] + libro.cant
                            adqui_cant_revista[carrera] = adqui_cant_revista[carrera] + 1
                        else: 
                            adqui_vol_revista[carrera] = libro.cant
                            adqui_cant_revista[carrera] = 1
    adquisiciones = {
        "volumen_libros": adqui_vol_libro,
        "cantidad_libros": adqui_cant_libro,
        "volumen_discos": adqui_vol_disco,
        "cantidad_discos": adqui_cant_disco,
        "volumen_revistas": adqui_vol_revista,
        "cantidad_revistas": adqui_cant_revista
    }
    # Obtiene información de los reportes de estadías
    reportes = model_estadias.objects.all()
    estadias_reportes = {}
    conc_carreras = {}
    contador = 1
    for reporte in reportes:
        if reporte.carrera not in estadias_reportes:
            estadias_reportes[reporte.carrera] = 1
        else:
            estadias_reportes[reporte.carrera] = contador
        contador += 1

    # Obtiene todas las carreras activas
    carreras = Carrera.objects.all()
    for carrera in carreras:
        # Evita que se agregen duplicados
        if carrera.abreviatura not in conc_carreras:
            # Valida que este 
            # if carrera.activo:
            conc_carreras[carrera.abreviatura] = carrera.nombre
    # Obtiene el número de visitas a los reportes de estadías
    views = register_view.objects.all()
    vistas_reportes = {}
    concentrado_vistas = []
    for view in views:
        # Busqueda relación de reporte por id
        for reporte in reportes:
            if view.id_reporte == reporte.id:
                data = {
                    'Matricula': view.matricula,
                    'Reporte': reporte.proyecto,
                    'Carrera': reporte.carrera,
                    'Fecha_cosul': view.fecha_consulta.strftime("%Y/%m/%d %H:%M:%S")
                }
                concentrado_vistas.append(data)
                # Valida si ya existe la información en el arreglo
                if reporte.proyecto in vistas_reportes:
                    # Obtiene el ultimo registro del contador agregado y le aumenta 1
                    cont_ant = vistas_reportes[reporte.proyecto][1]
                    vistas_reportes[reporte.proyecto] = [reporte.carrera, cont_ant + 1]
                else:
                    # Si no hay registro en el arreglo se crea uno nuevo iniciando en 1
                    vistas_reportes[reporte.proyecto] = [reporte.carrera, 1]

    # Se obtiene información de los prestamos
    prestamos = model_catalogo.objects.all()
    # fech_ini = '2024-12-01'
    # fech_fin = '2024-12-30'
    prestados_int = {}
    prestados_ext = {}
    noDevueltos_int = {}
    noDevueltos_ext = {}
    for prestamo in prestamos:
        for carrera in conteo_ejemplares:
            if str(prestamo.fechaP) >= fech_ini and str(prestamo.fechaP) <= fech_fin:
                # Libros prestados
                if not carrera in prestamo.colocacion:
                    continue
                if prestamo.tipoP == 'Interno':
                    if carrera in prestados_int:
                        # Obtiene dato anterior de prestamos
                        cant_ant = prestados_int[carrera]
                        prestados_int[carrera] = cant_ant + prestamo.cantidad_i
                        if prestamo.entrega == 'Entregado':
                            # Obtiene dato anterior de no devueltos
                            cant_ant_nd = noDevueltos_int[carrera]
                            noDevueltos_int[carrera] = cant_ant_nd + prestamo.cantidad_m
                    else:
                        # Se agrega dato en prestados
                        prestados_int[carrera] = prestamo.cantidad_i
                        if prestamo.entrega == 'Entregado':
                            # Se agrega datos en no devueltos
                            noDevueltos_int[carrera] = prestamo.cantidad_m
                elif prestamo.tipoP == 'Externo':
                    if carrera in prestados_ext:
                        # Obtiene dato anterior de prestamos
                        cant_ant = prestados_ext[carrera]
                        # Agrega nuevos valores
                        prestados_ext[carrera] = cant_ant + prestamo.cantidad_i
                        if prestamo.entrega == 'Entregado':
                            # Obtiene dato anterior de no devueltos
                            cant_ant_nd = noDevueltos_ext[carrera]
                            noDevueltos_ext[carrera] = cant_ant_nd + prestamo.cantidad_m

                    else:
                        prestados_ext[carrera] = prestamo.cantidad_i
                        if prestamo.entrega == 'Entregado':
                            noDevueltos_ext[carrera] = prestamo.cantidad_m
            
    prestamo_conc = {
        "prestados_int": prestados_int,
        "prestados_ext": prestados_ext,
        "noDevueltos_int": noDevueltos_int,
        "noDevueltos_ext": noDevueltos_ext
    }

    data = {
        'ciclo': ciclo,
        'cantidad_libro': cantidad_libro,
        'volumenes_por_libro': volumen_libro,
        'cantidad_disco': cantidad_disco,
        'volumenes_por_disco': volumen_disco,
        'cantidad_revista': cantidad_revista,
        'volumenes_por_revista': volumen_revista,
        'conteo_ejemplares': conteo_ejemplares,
        'conc_carreras': conc_carreras,
        'estadias_reportes': estadias_reportes,
        'cont_vistas_reporte': vistas_reportes,
        'concentrado_vistas': concentrado_vistas,
        'conc_adquisicion': conc_adquisicion,
        "adquisiciones": adquisiciones,
        "prestamo_conc": prestamo_conc
    }
    return generate_report(data)