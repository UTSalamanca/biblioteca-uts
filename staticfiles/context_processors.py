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
        return { 'grupo_abrev': '' }

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
    groups_list = ['Alumno', 'Biblioteca', '27 Docentes']
    # Verifica que el usuario este autenticado
    if user.is_authenticated:
        # Retorna el listado de todos los grupos en los que pertenece el usuario
        groups = user.groups.values_list('name', flat=True)
        # Recorre el listado de grupos
        # for i in range(0, len(groups)):
        #     # Valida que el grupo este dentro de los permitidos
        #     for g in range(0, len(groups_list)):
        #         if groups[i] == groups_list[g]:
        #             if query:
        #                 return groups[i]
        #             # Si el grupo es permitido se retorna
        #             if groups[i] == '27 Docentes':
        #                 grupo = groups[i].split(' ')[1]
        #                 return {"grupo": grupo}
        #             else:
        #                 return {"grupo": groups[i]}
        #         # else:
        #         #     return {"grupo": ""}
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

# def get_grupo(request):
#     gr = group_permission(request, True)
#     user = request.user
#     if gr != '27 Docentes' and gr != 'Biblioteca':
#         if user.is_authenticated:
#             grupos = []
#             cve_grupo = AlumnoGrupo.objects.filter(matricula=user.login).values_list('cve_grupo', flat=True)
#             for cve in cve_grupo:
#                 grupo_name = Grupo.objects.get(cve_grupo=cve)
#                 grupos.append(grupo_name.nombre)
#             for name_grupo in grupos[::-1]:
#                 if name_grupo:
#                     break
#             return {'grupo_name': name_grupo}
#         else:
#             return {'grupo_name': ''}
#     else:
#         return {'grupo_name': ''}