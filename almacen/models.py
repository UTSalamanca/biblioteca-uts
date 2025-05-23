from django.db import models
from django.utils.translation import gettext_lazy as _

class LongTextField(models.TextField):
    def db_type(self, connection):
        if connection.vendor == 'mysql':
            return 'LONGTEXT'
        return super().db_type(connection)

# Create your models here.
class acervo_model(models.Model):
    
    class State(models.TextChoices):
        EXCELENTE = 'Excelente', _('Excelente')
        BUENO = 'Bueno', _('Bueno')
        REGULAR = 'Regular', _('Regular')
        MALO = 'Malo', _('Malo')

    class Format(models.TextChoices):
        LIBRO = 'Libro', _('Libro')
        DISCO = 'Disco', _('Disco')
        REVISTA = 'Revista', _('Revista')

    titulo = models.CharField(max_length=200,verbose_name="titulo", null=True, blank=True)
    autor = models.CharField(max_length=200,verbose_name="Autor", null=True, blank=True)
    editorial = models.CharField(max_length=100,verbose_name="Editorial", null=True, blank=True)
    cant = models.IntegerField(verbose_name="Cantidad", null=True, blank=True)
    colocacion = models.CharField(max_length=100,verbose_name="Colocación", null=True, blank=True)
    edicion = models.CharField(max_length=100, verbose_name="Edición", null=True, blank=True)
    anio = models.CharField(max_length=20,verbose_name="Año de edición", null=True, blank=True)
    adqui = models.CharField(max_length=20,verbose_name="Tipo de adquisición", null=True, blank=True)
    estado = models.CharField(max_length=10, verbose_name="Estado", choices=State.choices, default=State.EXCELENTE, null=True, blank=True)
    formato = models.CharField(max_length=7, verbose_name="formato", choices=Format.choices, default=Format.LIBRO, null=True, blank=True)
    base64 = LongTextField('Portada',null=True,blank=True)
    fecharegistro = models.DateField(verbose_name="Fecha de Registro", auto_now_add=True)
    fechaedicion = models.DateField(verbose_name="Fecha de actualización", auto_now=True)

    def _str_(self):
        return self.titulo

    class Meta:
        verbose_name = 'Acervo registros'
