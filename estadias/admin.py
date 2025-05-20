from django.contrib import admin
from .models import model_estadias, register_view
# Register your models here.
# admin.site.register(model_estadias)

# Personalizando la vista del admin para Estadia
class estadia_admin(admin.ModelAdmin):
    list_display = ('proyecto', 'matricula','alumno' ,'asesor_academico' ,'generacion','empresa','asesor_orga','carrera')  # Los campos que se muestran en la lista
    list_filter = ('matricula', 'proyecto', 'carrera', 'alumno' ,'asesor_academico')  # Filtro por fecha de entrada

# Personalizando la vista del admin para Cliente
class view_admin(admin.ModelAdmin):
    list_display = ('id_reporte', 'matricula', 'consultas')  # Los campos que se muestran en la lista

# Registrando los modelos con sus clases personalizadas
admin.site.register(model_estadias, estadia_admin)
admin.site.register(register_view, view_admin)