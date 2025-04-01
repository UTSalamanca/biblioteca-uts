from django.shortcuts import render, redirect
from almacen.models import acervo_model
from catalogo.models import model_catalogo
from django.contrib import messages
from .forms import catalogo_form
import json
import base64
from django.http import JsonResponse
from django.utils.timezone import now, localtime
from sito.models import Alumno, AlumnoGrupo, Grupo, Carrera, Usuario, Persona, Periodo, Docente
from static.helpers import *

# Create your views here.
def catalago(request):
    """Función principal para mostrar la información en el index

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Arreglo con la información filtrada del catalogos
    """
    data_prestamo = 'Interno: Préstamos dentro de la universidad. Externo: Préstamos fuera de la universidad, con 6 días permitidos como límite.'
    form = catalogo_form()
    side_code = 400
    listado = acervo_model.objects.all()
    return render(request, 'index_catalogo.html', {"side_code": side_code, "listado":listado, "form":form, "data_prestamo": data_prestamo})

# Genera la vista para la tabla de prestamos
@groups_required('Administrador')
def prestamos_View(request):
    """Función para el recopialdo de la información para los dashboard y tablas de inicio

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Arreglo con la información formateada
    """
    side_code = 401
    listado = model_catalogo.objects.all()

    dias_permitidos = 6
    data = {}
    data_all = []
    cont = 0

    for f in listado:
        data = {
            "id": f.id,
            "cve_prestamo": f.cve_prestamo,
            "nom_alumno": f.nom_alumno,
            "matricula": f.matricula,
            "carrera_grupo": f.carrera_grupo,
            "nom_libro": f.nom_libro,
            "nom_autor": f.nom_autor,
            "colocacion": f.colocacion,
            "cantidad_i": f.cantidad_i,
            "cantidad_m": f.cantidad_m,
            "tipoP": f.tipoP,
            "entrega": f.entrega,
            "fechaP": f.fechaP,
            "fechaE": f.fechaE,
            "fechaD": f.fechaD,
        }   

        if f.tipoP == 'Externo':
            fecha_limite = f.fechaP
            # Fecha actual en la zona horaria configurada
            ahora = now().replace(microsecond=0)
            # Calculamos la diferencia entre las fechas
            diferencia = ahora - fecha_limite
            # Obtener el número de días de la diferencia
            dias_transcurridos = diferencia.days

            dias_restantes = dias_permitidos - dias_transcurridos

            data["dias_restantes"] = dias_restantes
            
        data_all.append(data)
    # print(json.dumps(data_all, sort_keys=False, indent=2))
    return render(request, 'index_prestamos.html', {"side_code": side_code, "data_all": data_all})

# obtiene datos de la persona por medio de su matricula o cve
def get_alumno(request):
    """Función para obtener la información especifica del alumno con respecto de la matricula

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Arreglo con la información filtrada del alumno
    """
    matricula = request.GET.get('matricula')
    if matricula:
        cve_persona = ''
        try:
            # Obtiene el listado de cve_grupo del alumno
            alumno_grupo = AlumnoGrupo.objects.filter(matricula=matricula).values_list('cve_grupo', flat=True)
            # Selecciona el ultimo en el que se ha registrado
            cve_grupo = alumno_grupo[len(alumno_grupo) - 1]
            # Realiza la busqueda del grupo con el cve_grupo
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
            persona = Persona.objects.get(cve_persona=request.user.cve_persona)
            data = {
                "nombre": persona.nombre,
                "apellido_paterno": persona.apellido_paterno,
                "apellido_materno": persona.apellido_materno,
                "nombre_grupo": "N/A",
                "nombre_carrera": "N/A",
                "generacion": "N/A"
            }
            return JsonResponse(data)
        except Exception as b:
            print(f"Algo salio mal: {b}")
    return JsonResponse({'error': 'Matricula o número de empleado no proporcionada'}, status=400)

# Genera clave unica para prestamo
def create_cve(fullname, colocacion):
    """Función para la creación de la clave (cve) única para el registro en las tablas

    Args:
        fullname (string): Nombre completo
        colocacion (string): Colocación

    Returns:
        string: Clave creada
    """
    cont = 1
    iniciales = ''
    coloca = ''
    # Valida que lleguen los datos
    if fullname and colocacion:
        # Obtiene las iniciales del nombre completo
        iniciales = "".join([palabra[0].upper() for palabra in fullname.split()])
        # Obtiene la colocación sin espacios
        coloca = colocacion.replace(" ", "")
        # Genera un bluque de busqueda
        while True:
            # Genera una sola clave
            cve = iniciales + coloca + str(cont)
            # Raliza una busqueda en base de datos
            cve_exist = model_catalogo.objects.filter(cve_prestamo=cve).first()
            if cve_exist:
                # Si ya existe la clave, realiza un incremento en un dato y repite
                cont += 1
                continue
            else:
                # Si la clave es unica, se rompe el bucle
                break
        return cve

# Función registra prestamos
def prestamo_registro(request):
    """Función para el registro en base de datos de los ejemplares prestados.

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        Void
    """
    try:
        if request.method == 'POST':
            form = catalogo_form(request.POST)
            if form.is_valid():
                # Se obtiene el número de libros existentes
                exist_book = acervo_model.objects.filter(titulo=form.cleaned_data['nom_libro'], colocacion=form.cleaned_data['colocacion']).first()
                if exist_book:
                    if exist_book.cant > 0:
                        if form.cleaned_data['cantidad_i'] < 0:
                            messages.add_message(request, messages.INFO, 'No puedes ingresar una cantidad negativa')
                            return redirect('catalago')
                        if form.cleaned_data['cantidad_i'] > exist_book.cant:
                            # Redirigir a la vista deseada
                            messages.add_message(request, messages.INFO, 'La solicitud excedió la cantidad de libros')
                            return redirect('catalago')
                        # Si la cantidad de los libros es mayor a 0, se realiza el prestamo
                        cve_prestamo = create_cve(form.cleaned_data['nom_alumno'], form.cleaned_data['colocacion'])
                        nom_libro = form.cleaned_data['nom_libro']
                        nom_autor = form.cleaned_data['nom_autor']
                        edicion = form.cleaned_data['edicion']
                        colocacion = form.cleaned_data['colocacion']
                        cantidad_i = form.cleaned_data['cantidad_i']
                        cantidad_m = form.cleaned_data['cantidad_i']
                        matricula = form.cleaned_data['matricula']
                        nom_alumno = form.cleaned_data['nom_alumno']
                        carrera_grupo = form.cleaned_data['carrera_grupo']
                        tipoP = form.cleaned_data['tipoP']
                        entrega = 'Proceso'
                        fechaP = now().replace(microsecond=0)

                        catalago=model_catalogo.objects.create(
                                cve_prestamo = cve_prestamo,
                                nom_libro = nom_libro,
                                nom_autor = nom_autor,
                                edicion = edicion,
                                colocacion = colocacion,
                                cantidad_i = cantidad_i,
                                cantidad_m = cantidad_m,
                                matricula = matricula,
                                nom_alumno = nom_alumno,
                                carrera_grupo = carrera_grupo,
                                tipoP = tipoP,
                                entrega = entrega,
                                fechaP = fechaP
                        )
                        # Se genera una redución de ejemplares en el acervo
                        exist_book.cant = exist_book.cant - cantidad_i
                        exist_book.save()

                        messages.add_message(request, messages.SUCCESS, 'Prestamo Solicitado')
                        # Redirigir a la vista deseada
                        return redirect('prestamos_usuario')
                    else:
                        messages.add_message(request, messages.INFO, 'Ejemplar agotado')
                        # Redirigir a la vista deseada
                        return redirect('catalago')    
                else:
                    messages.add_message(request, messages.INFO, 'Ejemplar no encontrado')
                    # Redirigir a la vista deseada
                    return redirect('catalago')
            else:
                # Si el formulario no es válido, vuelve a renderizar el formulario con errores
                messages.add_message(request, messages.ERROR, '¡Por favor, corrija los errores del formulario!')
                return redirect('catalago')
        else:
            # Si no es un POST, se asume que es un GET
            form = catalogo_form()
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('catalago')
    except Exception as p:
        print(p)
        return HttpResponse("¡El proceso no se pudo realizar!", status=400)

# Función para convertir documento a base64
def convert_base64(img):
    """Función para la conversión de una imagen en base64

    Args:
        img (object): Objeto de la imagen

    Returns:
        objeto: Objeto de la imagen convertida
    """
    try:
        imagen_base64 = base64.b64encode(img.read()).decode('utf-8')
        return imagen_base64
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró la imagen en la ruta: {ruta_imagen}")
    except Exception as e:
        raise Exception(f"Error al convertir la imagen a Base64: {e}")

# Función para convertir de base64 a imagen y presentarla
def view_book(request, base64):
    """Función para la creación del archivo de base64 a pdf

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        base64 (string): Bade64 de archivo a consultar

    Returns:
        Void
    """
    try:
        # Se obtienen los datos entrantes
        colocacion = request.GET.get('colocacion')
        base64 = request.GET.get('base64')
        titulo = request.GET.get('titulo')
        exist_book = acervo_model.objects.filter(colocacion=colocacion, base64=base64).first()
        if exist_book:
            # Se crea el archivo temporal y se obtiene la ruta
            name_temp = temporary_image_base64(base64, titulo, colocacion)
            # Se separan los datos no necesarios
            ruta = name_temp.split('/code')[1]
        else:
            messages.add_message(request, messages.ERROR, 'Libro no encontrado')
            return redirect('catalago')
    except Exception as vi:
        return redirect('catalago')

# Carga la vista con la información del acervo
@groups_required('Administrador')
def cargar_portada(request):
    """Muestra la información de catalogos

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Información filtrada
    """
    side_code = 402
    form = catalogo_form()
    return render(request, 'cargar_portada.html', {"form":form, "side_code": side_code})

# Función que realiza la edición del elemento con la imagen de portada
def edit_portada(request):
    """Función para realizar la actualización de portada

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        Void
    """
    if request.method == 'POST':
        data = {}
        cont = 1
        colocacion = ''
        # Se almacena la imagen entrante con el nombre del libro que le corresponde.
        for r in request.FILES:
            data[cont] = [r, request.POST.get(f"titulo-{cont}")]
            cont += 1

        # Se realiza el guardado de la imagen con el libro indicado
        for d in range(len(data)):
            # print(data[d+1][1]) # Se obtiene el nombre del libro

            # return redirect('cargar_portada')
            colocacion = request.POST.get('colocacion')  # Obtén la colocación del formulario
            nueva_portada = request.FILES[data[d+1][0]]  # Obtén el archivo subido

            if not colocacion or not nueva_portada:
                messages.add_message(request, messages.ERROR, 'Falta información: colocación o archivo de portada.')
                return redirect('cargar_portada')  # Redirige con un mensaje de error

            # Buscar el registro en la base de datos por `colocacion`
            acervo_update = acervo_model.objects.filter(colocacion=colocacion, titulo=data[d+1][1]).first()

            if acervo_update:
                # Almacenar el nuevo archivo de portada}
                acervo_update.base64 = convert_base64(nueva_portada)
                acervo_update.fechaedicion = now().replace(microsecond=0)
                acervo_update.save()
                
            else:
                messages.add_message(request, messages.ERROR, 'No se encontró un registro con la colocación proporcionada.')
                return redirect('cargar_portada')  # Redirige con un mensaje de error
        messages.add_message(request, messages.SUCCESS, 'Portada actualizada exitosamente.')
        return redirect('cargar_portada')  # Redirige al éxito
    else:
        messages.add_message(request, messages.ERROR, 'Solicitud inválida.')
        return redirect('cargar_portada')

# Se buscan lo libro por colocación
def search_book(request):
    """Realiza la busqueda de ejemplares

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Información filtrada del ejemplar
    """
    get_colocacion = request.GET.get('colocacion')
    if get_colocacion:
        try:
            book_data = {}
            data_all = []
            book = acervo_model.objects.all()
            for b in book:
                if b.colocacion == get_colocacion:
                    book_data = {
                        'colocacion': b.colocacion,
                        'titulo': b.titulo, 
                        'autor': b.autor,
                        'anio': b.anio,
                        'edicion': b.edicion,
                        'formato': b.formato
                    }
                    data_all.append(book_data)
            return JsonResponse({'status': 'success', 'books': data_all})

        except acervo_model.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'No colocacion provided'}, status=400)

# Cambia el estado de la entrega de los libros
def book_delivered(request, cve, entrega):
    """Cambia el estado de entrega de los ejemplares

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        cve (string): Clave del prestamos
        entrega (string): Estado actual del prestamos

    Returns:
        Void
    """
    try:
        book = model_catalogo.objects.filter(cve_prestamo=cve).first()
        if book:
            # Cambio de estado al ser entregado al solicitante
            if entrega == 'Proceso':
                # Se actualizan los campos necesario en el registro de prestamos
                book.entrega = 'Entregado'
                book.fechaE = now().replace(microsecond=0)
            # Se realiza la disminución de la cantidad en el acervo (si se corrige el estado)
            if entrega == 'Entregado':
                # Se actualizan los campos necesario en el registro de prestamos
                ref_catalogo = acervo_model.objects.filter(titulo=book.nom_libro, colocacion=book.colocacion).first()
                if ref_catalogo:
                    ref_catalogo.cant = ref_catalogo.cant + book.cantidad_m
                    ref_catalogo.save()
                else:
                    messages.add_message(request, messages.ERROR, 'No se encontro la referencia en acervo')
                    return redirect('prestamos_View')
                book.entrega = 'Devuelto'
                book.fechaD = now().replace(microsecond=0)
                book.cantidad_m = 0
            # Se guardan los cambios en la tabla del catalago
            book.save()

            messages.add_message(request, messages.SUCCESS, 'Estado del prestamo modificado')
            return redirect('prestamos_View')
        else:
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!.')
            return redirect('prestamos_View')
    except Exception as b:
        print(b)
        messages.add_message(request, messages.ERROR, 'No se pudo realizar la acción.')
        return redirect('prestamos_View')

# Vista, retorna todos los libros solicitados por el usuario
def prestamos_usuario(request):
    """Revuelve todos los libros solicitados por el usuario

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Información filtrada del ejemplar
    """
    side_code = 403
    try:
        ref_matricula = str(request.user)
        ref_persona = model_catalogo.objects.filter(matricula=ref_matricula)

        dias_permitidos = 6
        data = {}
        data_all = []
        cont = 0

        for f in ref_persona:
            data = {
                "id": f.id,
                "cve_prestamo": f.cve_prestamo,
                "nom_alumno": f.nom_alumno,
                "matricula": f.matricula,
                "carrera_grupo": f.carrera_grupo,
                "nom_libro": f.nom_libro,
                "nom_autor": f.nom_autor,
                "edicion": f.edicion,
                "colocacion": f.colocacion,
                "cantidad_m": f.cantidad_m,
                "tipoP": f.tipoP,
                "entrega": f.entrega,
                "fechaE": f.fechaE,
                "fechaD": f.fechaD,
                "fechaP": f.fechaP,
            }   

            if f.tipoP == 'Externo':
                fecha_limite = f.fechaP
                # Fecha actual en la zona horaria configurada
                ahora = now().replace(microsecond=0)
                # Calculamos la diferencia entre las fechas
                diferencia = ahora - fecha_limite
                # Obtener el número de días de la diferencia
                dias_transcurridos = diferencia.days

                dias_restantes = dias_permitidos - dias_transcurridos

                data["dias_restantes"] = dias_restantes
                
            data_all.append(data)
        return render(request, 'libros_pedidos.html', { "side_code": side_code, "data_all": data_all})
    except Exception as g:
        print(g)
        messages.add_message(request, messages.ERROR, 'No se encontro información.')
        return redirect('inicio')

# Cambia el estado de la entrega de los libros
def renew_again(request, cve, cant, entrega):
    """Manejo de la opción renovar prestamos

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP
        cve (string): Clave del prestamo
        cant (integer): Cantidad de ejemplares para solicitar de nuevo
        entrega (string): Estado del prestamo

    Returns:
        Void
    """
    try:
        book = model_catalogo.objects.filter(cve_prestamo=cve).first()
        if book:
            if entrega != 'Proceso':
                # Valida la cantidad de libros que se solicitan renovar
                # cant = int(cant)
                if entrega != 'Devuelto':
                    if cant < book.cantidad_m:
                        diferencia = book.cantidad_m - cant
                        # Se obtiene la referencia del libro en el acervo
                        ref_catalogo = acervo_model.objects.filter(titulo=book.nom_libro, colocacion=book.colocacion).first()
                        if ref_catalogo:
                            # Se aumenta la diferencia en la cantidad total
                            ref_catalogo.cant = ref_catalogo.cant + diferencia
                            ref_catalogo.save()
                        else:
                            messages.add_message(request, messages.ERROR, 'No se encontro la referencia en acervo')
                            return redirect('prestamos_View')
                        # Sere realiza el ajuste de libros en el catalogo
                        book.cantidad_m = book.cantidad_m - diferencia
                else:

                    # Se obtiene la referencia del libro en el acervo
                    ref_catalogo = acervo_model.objects.filter(titulo=book.nom_libro, colocacion=book.colocacion).first()
                    if ref_catalogo:
                        # Se aumenta la diferencia en la cantidad total
                        if cant > ref_catalogo.cant:
                            messages.add_message(request, messages.INFO, 'La cantidad soicitada, ya no esta disponible')
                            return redirect('prestamos_View')    
                        ref_catalogo.cant = ref_catalogo.cant - cant
                        ref_catalogo.save()
                    else:
                        messages.add_message(request, messages.ERROR, 'No se encontro la referencia en acervo')
                        return redirect('prestamos_View')
                    # Sere realiza el ajuste de libros en el catalogo
                    book.cantidad_m = cant
                    book.cantidad_i = cant
                    book.fechaD = None
                book.fechaP = now().replace(microsecond=0)
                book.fechaE = None
                book.entrega = 'Proceso'
                book.save()

                messages.add_message(request, messages.SUCCESS, 'Renovación exitosa')
                return redirect('prestamos_View')
            else:
                messages.add_message(request, messages.INFO, 'El libro aún no ha sido entregado')
                return redirect('prestamos_View')
        else:
            messages.add_message(request, messages.ERROR, '¡Algo salio mal!')
            return redirect('prestamos_View')
    except Exception as b:
        print(b)
        messages.add_message(request, messages.ERROR, 'No se pudo realizar la acción')
        return redirect('prestamos_View')

# Llega petición ajax, busqueda de cantidad por titulo y colocación
def cant_for_search(request):
    """Busca ejemplar en el acervo

    Args:
        request (object): Objeto que contiene la información sobre la solicitud HTTP

    Returns:
        array: Información filtrada de la cantidad de ejemplares
    """
    try:
        get_titulo = request.GET['titulo']
        get_colocacion = request.GET['colocacion']
        exist_element = acervo_model.objects.filter(titulo=get_titulo, colocacion=get_colocacion).first()
        if exist_element:
            return JsonResponse({'status': 'success', 'cantidad': exist_element.cant})
        else:
            return JsonResponse({'error': 'Elemento no encontrado'}, status=400)
    except Exception as s:
        return JsonResponse({'error': 'El proceso no se pudo realizar'}, status=400)