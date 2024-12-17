from typing import Any
from django.db import models
# from django_mysql.models import LongTextField

class LongTextField(models.TextField):
    def db_type(self, connection):
        if connection.vendor == 'mysql':
            return 'LONGTEXT'
        return super().db_type(connection)

class model_estadias(models.Model):

     proyecto=models.CharField(max_length=255)
     matricula=models.IntegerField()
     alumno=models.CharField(max_length=255)
     asesor_academico=models.CharField(max_length=255)
     generacion=models.CharField(max_length=255)
     empresa=models.CharField(max_length=255)
     asesor_orga=models.CharField(max_length=255)
     carrera = models.CharField(max_length=255)
     reporte=models.CharField(max_length=255,null=True)
     base64 = LongTextField('Reporte',null=True,blank=True)
     fecha_registro = models.DateTimeField(verbose_name="Fecha de registro", null=True, blank=True)

     def __str__(self):
          return self.alumno

     class Meta:
          verbose_name="estadía"
          verbose_name_plural='estadías'
          constraints = [
               models.UniqueConstraint(fields=['matricula', 'proyecto'], name='unique_matricula_proyecto')
          ]


class register_view(models.Model):
     id_reporte = models.IntegerField(null=True)
     matricula=models.IntegerField(null=True)
     consultas = models.IntegerField(null=True)
     fecha_consulta = models.DateTimeField(verbose_name="Fecha de consulta", null=True, blank=True)

     def __str__(self):
          return str(self.matricula)

     class Meta:
          verbose_name="consulta"
          verbose_name_plural='consultas'