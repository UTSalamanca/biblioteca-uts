from django.db import models
from django.utils.translation import gettext_lazy as _

class LongTextField(models.TextField):
    def db_type(self, connection):
        if connection.vendor == 'mysql':
            return 'LONGTEXT'
        return super().db_type(connection)
        
class model_catalogo(models.Model):

    class state_entrega(models.TextChoices):
        N_ENTREGADO = 'No/entregado', _('No/entregado')
        ENTREGADO = 'Entregado', _('Entregado')
        DEVUELTO = 'Devuelto', _('Devuelto')
        PROCESO = 'Proceso', _('Proceso')
    
    cve_prestamo=models.CharField(max_length=255, null=True)
    nom_libro=models.CharField(max_length=255)
    nom_autor=models.CharField(max_length=255)
    edicion=models.CharField(max_length=255)
    colocacion=models.CharField(max_length=255)
    formatoejem=models.CharField(max_length=255)
    cantidad_i=models.IntegerField()
    cantidad_m=models.IntegerField()
    matricula=models.IntegerField()
    nom_alumno=models.CharField(max_length=255)
    carrera_grupo=models.CharField(max_length=255)
    tipoP = models.CharField(max_length=255, null=True)
    fechaP = models.DateTimeField(verbose_name='Fecha prestamo', null=True, blank=True)
    entrega = models.CharField(max_length=255, verbose_name="Tipo de entrega", choices=state_entrega.choices, default=state_entrega.N_ENTREGADO, null=True, blank=True)
    fechaE = models.DateTimeField(verbose_name='Fecha entrega', null=True, blank=True)
    fechaD = models.DateTimeField(verbose_name='Fecha devuelto', null=True, blank=True)

    def _str_(self):
        return self.prestamos

    class Meta:
        verbose_name="prestamos"
        verbose_name_plural='prestamos'