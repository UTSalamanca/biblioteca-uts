from sito.models import Persona, AlumnoClase, AlumnoGrupo, Grupo

def persona(request):
   user = request.user
   if user.is_authenticated:
        persona = Persona.objects.get(cve_persona=user.cve_persona)
        return {'persona': persona}
   else:
        return {'persona': ''}

def grupo_alumno(request):
    user = request.user
    # Obtiene el listado de cve_grupo del alumno
    try:
        alumno_grupo = AlumnoGrupo.objects.filter(matricula=user.login).values_list('cve_grupo', flat=True)
        # Selecciona el ultimo en el que se ha registrado
        cve_grupo = alumno_grupo[len(alumno_grupo) - 1]
        # Realiza la busqueda del grupo con el cve_grupo
        grupo = Grupo.objects.get(cve_grupo=cve_grupo)
        return { 'grupo_abrev': grupo.nombre }
    except:
        return { 'grupo_abrev': 'NA' }

def iniciales_nombre(request):
   user = request.user
   iniciales = ''
   if user.is_authenticated:
        persona = Persona.objects.get(cve_persona=user.cve_persona)
        iniciales = "".join([palabra[0].upper() for palabra in persona.nombre.split()])
        return {'iniciales': iniciales}
   else:
        return {'iniciales': ''}

def user_permissions_and_groups(request):
   # Check if the user is authenticated
   if request.user.is_authenticated:
       # Get the user's permissions and groups
       permissions = request.user.get_all_permissions()
       groups = request.user.groups.values_list('name', flat=True)
   else:
       permissions = set()
       groups = []


   return {
       'user_permissions': permissions,
       'user_groups': groups,
   }

def group_permission(request, query = False):
    user = request.user
    # Verifica que el usuario este autenticado
    if user.is_authenticated:
        # Retorna el listado de todos los grupos en los que pertenece el usuario
        groups = user.groups.values_list('name', flat=True)
        if groups:
            return {"grupo_control": groups}
    else:
        # Si el usuario no esta autenticado, se retorna una variable vacía
        return {"grupo": ""}

def get_alumnos_clase(request):
    user = request.user
    r = []
    if user.is_authenticated:
        alumnos = AlumnoClase.objects.filter(matricula=user.login).values_list('cve_docente', flat=True)
        for al in alumnos:
            if al not in r:
                r.append(al)
        return {'profesor': r}
    else:
        return {'profesor': ''}