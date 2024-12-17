from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from sistema.models import UsuarioAcceso
from sito.models import Usuario, UsuarioGrupoSeguridad
from usuario.forms import LoginForm, RegisterUserForm, PerfilForm
from static.helpers import dd
from sito.models import Persona
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = LoginForm(request.POST or None)  # Instanciar el formulario

    if request.method == 'POST':
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']

            # Buscar si el usuario existe en sistema_usuario
            sistema_usuario = UsuarioAcceso.objects.filter(login=login).first()
            if sistema_usuario is not None:
                # persona = Persona.objects.get(cve_persona=sistema_usuario.cve_persona)
                # Si el usuario existe en sistema_usuario, intentamos autenticarlo
                usuario = authenticate(request, login=login, password=password)
                print(f"User: {usuario}")
                if usuario is not None:
                    # Usuario autenticado, iniciar sesión y redirigir
                    auth_login(request, sistema_usuario)
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    return redirect("inicio")
                else:
                    # Credenciales incorrectas
                    # messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
                    messages.add_message(request, messages.ERROR, 'Por favor introduzca un nombre de usuario y contraseña correctos.')
                    return redirect('login')
            else:
                # El usuario no existe en sistema_usuario, buscar en Usuario
                usuario_existente = Usuario.objects.filter(login=login, password=password).first()

                if usuario_existente is not None:
                    # Usuario encontrado en Usuario, crear en sistema_usuario
                    sistema_usuario = UsuarioAcceso.objects.create(
                        cve_persona=usuario_existente.cve_persona,
                        login=usuario_existente.login,
                        activo=True,
                        staff=True
                    )
                    sistema_usuario.set_password(password)
                    sistema_usuario.save()

                    # Obtener los grupos de seguridad del usuario
                    usuario_grupo_seguridad = UsuarioGrupoSeguridad.objects.filter(cve_persona=usuario_existente.cve_persona)

                    for grupo in usuario_grupo_seguridad:
                        group, created = Group.objects.get_or_create(name=grupo.cve_grupo_seguridad)
                        sistema_usuario.groups.add(group)

                    # Iniciar sesión con el nuevo usuario en sistema_usuario
                    auth_login(request, sistema_usuario)
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    return redirect("inicio")
                else:
                    # El usuario no existe en ninguna de las tablas
                    # messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
                    messages.add_message(request, messages.ERROR, 'Por favor introduzca un nombre de usuario y contraseña correctos.')
                    return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'index_login.html', context)

def logout_view(request):
    auth_logout(request)
    # Redirigir a la página de inicio o cualquier otra página deseada después del logout
    return redirect('usuario:login')

@login_required(login_url='usuario:login')
def perfil_view(request):
    user_perfil = UsuarioAcceso.objects.get(login=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user_perfil)
        if form.is_valid():
            if request.FILES.get('avatar'):
                if request.user.avatar.name.endswith('default.png'):
                    # Si el avatar es default.png conservar imagen predeterminada.
                    form.save()
                    # messages.success(request, '¡Tu perfil ha sido actualizado!')
                    messages.add_message(request, messages.SUCCESS, '¡Tu perfil ha sido actualizado!')
                else:
                    # Si el avatar es diferente a default.png eliminar la imagen.
                    request.user.avatar.delete()
                    form.save()
                    # messages.success(request, '¡Tu perfil ha sido actualizado!')
                    messages.add_message(request, messages.SUCCESS, '¡Tu perfil ha sido actualizado!')
            else:
                # Conservar imagen actual en caso de no haber seleccionado otra.
                user_perfil.avatar = user_perfil.avatar
                user_perfil.save()
                # messages.warning(request, 'No seleccionaste una nueva imagen. Tu perfil no ha sido actualizado.')
                messages.add_message(request, messages.WARNING, 'No seleccionaste una nueva imagen. Tu perfil no ha sido actualizado.')
            return redirect("usuario:perfil")
        else:
            # messages.error(request, 'Por favor corrige los errores del formulario.')
            messages.add_message(request, messages.ERROR, 'Por favor corrige los errores del formulario.')
    else:
        form = PerfilForm(instance=user_perfil)
    return render(request, 'usuario/perfil.html', {'form': form})

