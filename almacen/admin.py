from django.contrib import admin
from .models import acervo_model
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources
from .forms import registro_form
from django.contrib.auth.admin import UserAdmin

class acervo_admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('titulo','autor','editorial','cant','colocacion','edicion','anio','adqui','formato','estado', 'base64', 'fecharegistro', 'fechaedicion') 
    list_filter = ('colocacion', 'adqui', 'formato', 'estado')  # Filtro por fecha de entrada

admin.site.register(acervo_model, acervo_admin)