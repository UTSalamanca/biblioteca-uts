from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group

from sistema.models import UsuarioAcceso
from sistema.forms import UsuarioAccesoChangeForm
from sito.models import Persona

### @admin.register(UsuarioAcceso)
### class UsuarioAccesoAdmin(DjangoUserAdmin):
###     form = UsuarioAccesoChangeForm
### 
###     list_display = (
###         'cve_persona', 'login', 'get_nombre_completo', 'email', 'activo', 'staff', 'superuser', 'date_joined',
###     )
### 
###     def get_nombre_completo(self, obj):
###         persona = Persona.objects.get(cve_persona=obj.cve_persona)
###         return persona.nombre_completo()
### 
###     search_fields = ('login', 'email',)
### 
###     list_filter = ('activo', 'staff', 'superuser')
### 
###     ordering = ('login',)
### 
###     readonly_fields = ['login', 'last_login', 'date_joined']
### 
###     fieldsets = (
###         (None, {'fields': ('login', 'password', 'email', 'avatar')}),
###         # (_('Datos Generales'), {'fields': ('nombre', 'apellido_paterno',
###         #  'apellido_materno', 'email')}),
###         # (_('Domicilio Actual'), {'fields': (
###         #     'estado', 'ciudad', 'colonia', 'calle', 'num_exterior', 'num_interior')}),
###         (_('Permissions'), {
###             'fields': ('activo', 'staff', 'superuser', 'groups', 'user_permissions'),
###         }),
###         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
###     )
### 
###     add_fieldsets = (
###         (None, {
###             'classes': ('wide',),
###             'fields': ('login', 'password1', 'password2', 'email'),
###         }),
###         # (_('Datos Generales'), {'fields': ('nombre', 'apellido_paterno',
###         #  'apellido_materno', 'email')}),
###         # (_('Domicilio Actual'), {'fields': (
###         #     'estado', 'ciudad', 'colonia', 'calle', 'num_exterior', 'num_interior')}),
###         (_('Permissions'), {
###             'fields': ('activo', 'staff', 'superuser', 'groups', 'user_permissions'),
###         }),
###     )
### 
###     def has_add_permission(self, request, obj=None):
###         return False
### 
###     def has_delete_permission(self, request, obj=None):
###         return False





# @admin.register(SistemaUsuarioAccesoGroups)
# class SistemaUsuarioAccesoGroupsAdmin(DjangoUserAdmin):
#     list_display = (
#         'id', 'usuarioaccesso_id', 'group_id',
#     )