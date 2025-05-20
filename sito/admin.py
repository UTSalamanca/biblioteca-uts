from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group

# Register your models here.

### from sito.models import (
###     Usuario as UsuarioSito,
###     GrupoSeguridad,
###     UsuarioGrupoSeguridad,
###     Persona as PersonaSito,
###     Periodo,
###     Pais,
###     Ciudad,
###     Estado,
###     EstadoCivil,
###     ReferenciasBanco
### )

# class DatabaseSitoModelAdmin(admin.ModelAdmin):
#     using = 'sito'

#     def save_model(self, request, obj, form, change):
#         # Tell Django to save objects to the 'other' database.
#         obj.save(using=self.using)

#     def delete_model(self, request, obj):
#         # Tell Django to delete objects from the 'other' database
#         obj.delete(using=self.using)

#     def get_queryset(self, request):
#         # Tell Django to look for objects on the 'other' database.
#         return super().get_queryset(request).using(self.using)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Tell Django to populate ForeignKey widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Tell Django to populate ManyToMany widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

# class DatabaseSitoTabularInline(admin.TabularInline):
#     using = 'sito'

#     def get_queryset(self, request):
#         # Tell Django to look for inline objects on the 'other' database.
#         return super().get_queryset(request).using(self.using)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Tell Django to populate ForeignKey widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         # Tell Django to populate ManyToMany widgets using a query
#         # on the 'other' database.
#         return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

### class UsuarioGrupoSeguridadInline(admin.TabularInline):
###     model = UsuarioGrupoSeguridad
###     extra = 0
### 
###     def has_add_permission(self, request, obj=None):
###         return False
### 
###     def has_change_permission(self, request, obj=None):
###         return False
### 
###     def has_delete_permission(self, request, obj=None):
###         return False
### 
### @admin.register(UsuarioSito)
### class UsuarioSitoAdmin(admin.ModelAdmin):
###     inlines = [UsuarioGrupoSeguridadInline]
### 
###     list_display = (
###         'cve_persona', 'login', 'password', 'activo',
###     )
### 
###     search_fields = ('login', 'cve_persona')
### 
###     list_filter = ('activo',)
### 
###     # readonly_fields = ('cve_persona', 'login', 'password',)
### 
###     # fieldsets = (
###     #     (None, {'fields': ('cve_persona', 'login', 'password', 'activo')}),
###     #     )
### 
###     # def has_add_permission(self, request, obj=None):
###     #     return False
### 
###     # def has_change_permission(self, request, obj=None):
###     #     return False
### 
###     # def has_delete_permission(self, request, obj=None):
###     #     return False
### 
### class GrupoSeguridadResource(resources.ModelResource):
###     class Meta:
###         model = GrupoSeguridad
###         fields = ('cve_grupo_seguridad', 'nombre',)
###         export_order = ('cve_grupo_seguridad', 'nombre',)
### 
### 
### @admin.register(GrupoSeguridad)
### class GrupoSeguridadAdmin(ExportMixin, admin.ModelAdmin):
###     resource_class = GrupoSeguridadResource
### 
###     list_display = (
###         'nombre', 'tiempo_sesion', 'activo',
###     )
### 
###     search_fields = ('nombre',)
### 
###     list_filter = ('activo',)
### 
###     ordering = ('cve_grupo_seguridad',)
### 
###     readonly_fields = ('cve_grupo_seguridad', 'nombre', 'tiempo_sesion', 'activo')
### 
###     fieldsets = (
###         (None, {'fields': ('cve_grupo_seguridad', 'nombre', 'tiempo_sesion', 'activo')}),
###         )
### 
###     def has_add_permission(self, request, obj=None):
###         return False
### 
###     def has_change_permission(self, request, obj=None):
###         return False
### 
###     def has_delete_permission(self, request, obj=None):
###         return False
### 
### class GroupResource(resources.ModelResource):
###     class Meta:
###         model = Group
###         fields = ('id', 'name',)
###         export_order = ('id', 'name',)
### 
### class GroupAdmin(ImportExportModelAdmin, DjangoGroupAdmin):
###     resource_class = GroupResource
###     search_fields = ('name',)
###     ordering = ('name',)
### 
### @admin.register(PersonaSito)
### class PersonaSitoAdmin(admin.ModelAdmin):
### 
###     list_display = (
###         'cve_persona', 'nombre_completo', 'mail', 'fecha_nacimiento',
###     )
### 
###     search_fields = ('nombre', 'apellido_paterno', 'apellido_materno',)
### 
###     # readonly_fields = ('cve_persona', 'login', 'password',)
### 
###     # fieldsets = (
###     #     (None, {'fields': ('cve_persona', 'login', 'password', 'activo')}),
###     #     )
### 
###     # def has_add_permission(self, request, obj=None):
###     #     return False
### 
###     # def has_change_permission(self, request, obj=None):
###     #     return False
### 
###     # def has_delete_permission(self, request, obj=None):
###     #     return False
### 
### @admin.register(Periodo)
### class PeriodoAdmin(admin.ModelAdmin):
###     list_display = ('nombre_periodo', 'fecha_inicio', 'fecha_fin', 'activo')
### 
###     def has_add_permission(self, request, obj=None):
###         return False
### 
###     def has_change_permission(self, request, obj=None):
###         return False
### 
###     def has_delete_permission(self, request, obj=None):
###         return False
### 
### @admin.register(ReferenciasBanco)
### class ReferenciasBancoAdmin(admin.ModelAdmin):
###     list_display = ('concepto', 'mensaje', 'cve_periodo')
### 
### admin.site.unregister(Group)
### admin.site.register(Group, GroupAdmin)
### admin.site.register(Pais)
### admin.site.register(Ciudad)
### admin.site.register(EstadoCivil)
### admin.site.register(Estado)