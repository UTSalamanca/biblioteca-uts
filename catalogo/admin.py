from django.contrib import admin
from .models import model_catalogo

# Personalizando la vista del admin para Estadia
class catalogo_admin(admin.ModelAdmin):
    list_display = ('cve_prestamo', 'nom_libro', 'nom_autor', 'edicion' ,'colocacion', 'cantidad_i', 'cantidad_m', 'matricula', 'nom_alumno', 'carrera_grupo', 'tipoP', 'fechaP', 'entrega', 'fechaE')  # Los campos que se muestran en la lista
    list_filter = ('cve_prestamo', 'colocacion', 'matricula', 'tipoP', 'fechaP', 'entrega', 'fechaE')  # Filtro por fecha de entrada

# Registrando los modelos con sus clases personalizadas
admin.site.register(model_catalogo, catalogo_admin)