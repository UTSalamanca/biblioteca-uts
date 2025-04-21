import random
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.contrib import messages
from sistema.models import UsuarioAcceso
from sito.models import Usuario, UsuarioGrupoSeguridad
from usuario.forms import LoginForm, RegisterUserForm, PerfilForm
from django.conf import settings

def enviar_codigo_verificacion(request, usuario):
    """Función para enviar el código de verificación por correo y gestionar la sesión."""
    codigo_verificacion = random.randint(100000, 999999)
    
    # Guardar datos en la sesión
    request.session['codigo_verificacion'] = codigo_verificacion
    request.session['codigo_creado'] = now().isoformat()
    request.session['usuario_id'] = usuario.cve_persona
    request.session['login'] = usuario.login

    # Preparar datos para el correo
    context = {
        'usuario': usuario,
        'codigo_verificacion': codigo_verificacion
    }
    
    # Dirección de correo (modificar si es necesario)
    # print(settings.DEBUG)
    # if settings.DEBUG:
    #     email = 'jrazo@utsalamanca.edu.mx'
    # else:
    email = f"{usuario.login}@utsalamanca.edu.mx"

    # Enviar correo
    user_email = email
    subject = "SIESAV - VERIFICACIÓN DE CUENTA"
    html_content = render_to_string('login/notification_verify_account.html', context)

    email = EmailMessage(subject, html_content, to=[user_email])
    email.content_subtype = "html"
    email.send()

    return True

def login_view(request):
    # Si la sesión tiene un código de verificación redirigir a la vista de verificación
    if request.session.get('codigo_verificacion'):
        return redirect('usuario:verify_account')
        
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', 'inicio:inicio'))

    form = LoginForm(request.POST or None)
    show_modal_login_success = False

    if request.method == 'POST' and form.is_valid():
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']

        # Primero buscar si el usuario existe en la tabla Usuario
        usuario_existente = Usuario.objects.filter(login=login, password=password).first()

        if usuario_existente:
            # Usuario existe en Usuario, ahora verificar en UsuarioAcceso
            sistema_usuario = UsuarioAcceso.objects.filter(login=usuario_existente.login).first()

            if sistema_usuario:
                # Usuario existe en UsuarioAcceso, verificar si las contraseñas están sincronizadas
                if not check_password(usuario_existente.password, sistema_usuario.password):
                    # Actualizar contraseña en UsuarioAcceso si es diferente
                    sistema_usuario.set_password(usuario_existente.password)
                    sistema_usuario.save()

                # Intentar autenticar con el usuario en UsuarioAcceso
                usuario = authenticate(request, username=login, password=password)
                if usuario:
                    # Verificar si el usuario pertenece al grupo 'Alumno' y enviar código de verificación
                    if usuario.groups.filter(name='Alumno').exists():
                        show_modal_login_success = enviar_codigo_verificacion(request, usuario)
                    else:
                        auth_login(request, usuario)
                        return redirect(request.GET.get('next', 'inicio:inicio'))
                else:
                    # messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
                    messages.add_message(request, messages.ERROR, 'Por favor introduzca un nombre de usuario y contraseña correctos.')
                    return redirect('usuario:login')

            else:
                # Usuario no existe en UsuarioAcceso, así que creamos el usuario
                sistema_usuario = UsuarioAcceso.objects.create(
                    cve_persona=usuario_existente.cve_persona,
                    login=usuario_existente.login,
                    activo=True,
                    staff=True
                )
                sistema_usuario.set_password(password)
                sistema_usuario.save()

                # Obtener los grupos de seguridad del usuario y asignarlos
                usuario_grupo_seguridad = UsuarioGrupoSeguridad.objects.filter(cve_persona=usuario_existente.cve_persona)
                for grupo in usuario_grupo_seguridad:
                    group, created = Group.objects.get_or_create(name=grupo.cve_grupo_seguridad)
                    sistema_usuario.groups.add(group)
                    
                if sistema_usuario.groups.filter(name='Alumno').exists():
                    show_modal_login_success = enviar_codigo_verificacion(request, sistema_usuario)
                    
                else:
                    auth_login(request, sistema_usuario)
                    return redirect(request.GET.get('next', 'inicio:inicio'))
        else:
            # Usuario no existe en la tabla Usuario
            # messages.error(request, "Por favor introduzca un nombre de usuario y contraseña correctos.")
            messages.add_message(request, messages.ERROR, 'Por favor introduzca un nombre de usuario y contraseña correctos.')
            return redirect('usuario:login')
        
    return render(request, 'login/login.html', {'form': form, 'show_modal_login_success': show_modal_login_success})

def verify_account_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', 'inicio:inicio'))
    
    # Recuperar los datos de la sesión
    usuario_id = request.session.get('usuario_id')
    login = request.session.get('login')
    codigo_verificacion = request.session.get('codigo_verificacion')
    codigo_creado = request.session.get('codigo_creado')
    
    if not usuario_id or not login or not codigo_verificacion or not codigo_creado:
        # messages.error(request, 'La sesión es inválida. Por favor, inicie sesión nuevamente.')
        messages.add_message(request, messages.ERROR, 'La sesión es inválida. Por favor, inicie sesión nuevamente.')
        return redirect('usuario:login')
    
    # Verificar si el código ha expirado
    codigo_creado_dt = now() if not codigo_creado else now().fromisoformat(codigo_creado)
    if now() > codigo_creado_dt + timedelta(minutes=5):
        # Limpiar la sesión y redirigir si ha expirado
        request.session.flush()
        # messages.error(request, 'El código de verificación ha expirado. Por favor, inicie sesión nuevamente.')
        messages.add_message(request, messages.ERROR, 'El código de verificación ha expirado. Por favor, inicie sesión nuevamente.')
        return redirect('usuario:login')
    
    email = f"{login}@utsalamanca.edu.mx"
    email_protegido = (
        f"{email.split('@')[0][:3]}*{email.split('@')[0][-3:]}@{email.split('@')[1]}"
        if '@' in email else "correo_invalido@dominio.com"
    )
    
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo_verificacion')

        if not codigo_ingresado.isdigit():
            # messages.error(request, 'El código de verificación debe contener solo números.')
            messages.add_message(request, messages.ERROR, 'El código de verificación debe contener solo números.')
            return redirect('usuario:verify_account')

        if codigo_ingresado and int(codigo_ingresado) == codigo_verificacion:
            usuario = UsuarioAcceso.objects.get(cve_persona=usuario_id)
            request.session.pop('codigo_verificacion', None)
            auth_login(request, usuario)
            return redirect(request.GET.get('next', 'inicio:inicio'))
        else:
            # messages.error(request, 'El código de verificación es incorrecto.')
            messages.add_message(request, messages.ERROR, 'El código de verificación es incorrecto.')
    
    return render(request, 'login/verify_account.html', {'email': email_protegido})


def logout_view(request):
    auth_logout(request)
    request.session.flush()
    # messages.success(request, 'Sesión cerrada exitosamente.')
    messages.add_message(request, messages.SUCCESS, 'Sesión cerrada exitosamente.')
    return redirect('usuario:login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        try:
            if form.is_valid():
                usuario_sito = Usuario.objects.get(login = request.POST['login'])
                usuario_grupo_seguridad = UsuarioGrupoSeguridad.objects.filter(cve_persona = usuario_sito.cve_persona)
                user = UsuarioAcceso(
                    cve_persona = usuario_sito.cve_persona,
                    login = form.cleaned_data.get('login'),
                    email = form.cleaned_data.get('email'),
                    activo = True,
                    staff = True
                )
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                for grupo in usuario_grupo_seguridad:
                    group, created = Group.objects.get_or_create(name=grupo.cve_grupo_seguridad)
                    user.groups.add(group)
                # for obj in usuario_grupo_seguridad:
                #     user.groups.add(obj.cve_grupo_seguridad.cve_grupo_seguridad)
                auth_login(request, user)
                messages.success(request, '¡Registro Exitoso!')
                return redirect("index")
        except Usuario.DoesNotExist:
            print("El usuario no existe.")
            messages.warning(request, 'La matrícula o número de empleado que quieres registrar no existe. Favor de ingresar un nombre de usuario válido.')
    else:
        form = RegisterUserForm()
    return render(request=request, template_name="login/register.html", context={"form": form})

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
                    messages.success(request, '¡Tu perfil ha sido actualizado!')
                else:
                    # Si el avatar es diferente a default.png eliminar la imagen.
                    request.user.avatar.delete()
                    form.save()
                    messages.success(request, '¡Tu perfil ha sido actualizado!')
            else:
                # Conservar imagen actual en caso de no haber seleccionado otra.
                user_perfil.avatar = user_perfil.avatar
                user_perfil.save()
                messages.warning(request, 'No seleccionaste una nueva imagen. Tu perfil no ha sido actualizado.')
            return redirect("usuario:perfil")
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = PerfilForm(instance=user_perfil)
    return render(request, 'login/perfil.html', {'form': form})