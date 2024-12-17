from django.db import models
from django.conf import settings


# Create your models here.

class Usuario(models.Model):
    cve_persona = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'usuario'
        verbose_name = 'Usuario SITO'
        verbose_name_plural = 'Usuarios SITO'

    def __str__(self):
        return f'{self.login}'

class GrupoSeguridad(models.Model):
    cve_grupo_seguridad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)
    tiempo_sesion = models.IntegerField()
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'grupo_seguridad'
        verbose_name = 'Grupo Seguridad'
        verbose_name_plural = 'Grupo Seguridad'

    def __str__(self):
        return f'{self.nombre}'

class UsuarioGrupoSeguridad(models.Model):
    cve_persona = models.OneToOneField(Usuario, models.DO_NOTHING, db_column='cve_persona', primary_key=True)
    cve_grupo_seguridad = models.ForeignKey(GrupoSeguridad, models.DO_NOTHING, db_column='cve_grupo_seguridad')

    class Meta:
        managed = False
        db_table = 'usuario_grupo_seguridad'
        unique_together = (('cve_persona', 'cve_grupo_seguridad'),)
        verbose_name = 'Usuario Grupo Seguridad'
        verbose_name_plural = 'Usuario Grupo Seguridad'

class Persona(models.Model):
    cve_persona = models.IntegerField(primary_key=True)
    cve_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='cve_pais')
    cve_ciudad = models.ForeignKey('Ciudad', models.DO_NOTHING, db_column='cve_ciudad')
    cve_estado_civil = models.ForeignKey('EstadoCivil', models.DO_NOTHING, db_column='cve_estado_civil')
    nombre = models.CharField(max_length=60)
    apellido_paterno = models.CharField(max_length=40, blank=True, null=True)
    apellido_materno = models.CharField(max_length=40, blank=True, null=True)
    mail = models.CharField(max_length=60, blank=True, null=True)
    movil = models.CharField(max_length=20, blank=True, null=True)
    rfc = models.CharField(max_length=15)
    curp = models.CharField(max_length=18, blank=True, null=True)
    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateTimeField()

    class Meta:
        app_label = 'sito'
        managed = False
        db_table = 'persona'

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    def __str__(self):
        return self.nombre_completo()

class Pais(models.Model):
    cve_pais = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=40)
    abreviatura = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        return f'{self.nombre}'

class Estado(models.Model):
    cve_estado = models.SmallIntegerField(primary_key=True)
    cve_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='cve_pais')
    nombre = models.CharField(max_length=40)
    abreviatura = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'

    def __str__(self):
        return f'{self.nombre}'

class Ciudad(models.Model):
    cve_ciudad = models.SmallIntegerField(primary_key=True)
    cve_estado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='cve_estado')
    nombre = models.CharField(max_length=50)
    lada = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ciudad'

    def __str__(self):
        return f'{self.nombre}'

class EstadoCivil(models.Model):
    cve_estado_civil = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'estado_civil'

    def __str__(self):
        return f'{self.nombre}'

MESES = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre',
}

class Periodo(models.Model):
    cve_periodo = models.SmallIntegerField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    fecha_inicio_clases = models.DateTimeField()
    fecha_fin_clases = models.DateTimeField()
    numero_periodo = models.IntegerField()
    no_extras = models.IntegerField(blank=True, null=True)
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'periodo'

    def nombre_periodo(self):
        nombre_mes_inicio = MESES.get(self.fecha_inicio.strftime('%B').capitalize())
        nombre_mes_fin = MESES.get(self.fecha_fin.strftime('%B').capitalize())
        anio = self.fecha_inicio.year
        if nombre_mes_inicio == nombre_mes_fin:
            nombre_periodo = f"{nombre_mes_inicio} {anio}"
        else:
            nombre_periodo = f"{nombre_mes_inicio} - {nombre_mes_fin} {anio}"
        return nombre_periodo

    def __str__(self):
        return f'{self.nombre_periodo()}'

    nombre_periodo.admin_order_field = 'fecha_inicio'
    nombre_periodo.short_description = 'Nombre del periodo'

class ReferenciasBanco(models.Model):
    cve_referencia = models.BigAutoField(primary_key=True)
    concepto = models.CharField(max_length=255, blank=True, null=True)
    matricula = models.CharField(max_length=255, blank=True, null=True)
    accion = models.CharField(max_length=255, blank=True, null=True)
    referencia = models.CharField(unique=True, max_length=255, blank=True, null=True)
    banco_emisor = models.CharField(max_length=255, blank=True, null=True)
    servicio_bb = models.CharField(max_length=255, blank=True, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    forma_pago = models.CharField(max_length=255, blank=True, null=True)
    monto_parcial_minimo = models.DecimalField(max_digits=8, decimal_places=2)
    firma = models.TextField(blank=True, null=True)
    estatus = models.CharField(max_length=255, blank=True, null=True)
    mensaje = models.CharField(max_length=255, blank=True, null=True)
    monto_original = models.DecimalField(max_digits=8, decimal_places=2)
    recargo_aplicado = models.DecimalField(max_digits=8, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=8, decimal_places=2)
    monto_a_pagar = models.DecimalField(max_digits=8, decimal_places=2)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    no_recibo = models.CharField(max_length=255, blank=True, null=True)
    folio_pago = models.CharField(max_length=255, blank=True, null=True)
    fecha_limite_pago = models.CharField(max_length=10, blank=True, null=True)
    fecha_pago = models.CharField(max_length=10, blank=True, null=True)
    hora_pago = models.CharField(max_length=16, blank=True, null=True)
    folio_reverso = models.CharField(max_length=255, blank=True, null=True)
    fecha_reverso = models.CharField(max_length=10, blank=True, null=True)
    hora_reverso = models.CharField(max_length=16, blank=True, null=True)
    cve_periodo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'referencias_banco'

    def __str__(self):
        return self.concepto

class Carrera(models.Model):
    cve_carrera = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    abreviatura = models.CharField(max_length=3, blank=True, null=True)
    activo = models.BooleanField()
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carrera'

    def __str__(self):
        return f'{self.nombre}'

class Grupo(models.Model):
    cve_grupo = models.SmallIntegerField(primary_key=True)
    cve_periodo = models.ForeignKey('Periodo', models.DO_NOTHING, db_column='cve_periodo', blank=True, null=True)
    cve_especialidad = models.SmallIntegerField()
    cve_carrera = models.ForeignKey('Carrera', models.DO_NOTHING, db_column='cve_carrera', blank=True, null=True)
    nombre = models.CharField(max_length=10)
    numero_cuatrimestre = models.SmallIntegerField()
    cve_turno = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'grupo'

class AlumnoGrupo(models.Model):
    matricula = models.OneToOneField('Alumno', models.DO_NOTHING, db_column='matricula', primary_key=True)
    cve_grupo = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='cve_grupo')


    class Meta:
        managed = False
        db_table = 'alumno_grupo'
        unique_together = (('matricula', 'cve_grupo'),)

    def __str__(self):
        return f'{self.matricula}'


class Alumno(models.Model):
    cve_alumno = models.IntegerField()
    matricula = models.CharField(primary_key=True, max_length=12)
    fecha_ingreso = models.DateTimeField()
    status = models.CharField(max_length=2)
    generacion = models.CharField(max_length=6, blank=True, null=True)
    status_academico = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'alumno'

class Clase(models.Model):
    cve_docente = models.ForeignKey('Docente', models.DO_NOTHING, db_column='cve_docente')
    cve_clase = models.IntegerField(primary_key=True)
    cve_periodo = models.ForeignKey('MateriaPlanPeriodo', models.DO_NOTHING, db_column='cve_periodo', blank=True, null=True, related_name='periodo_Clase_set')
    cve_materia = models.ForeignKey('MateriaPlanPeriodo', models.DO_NOTHING, db_column='cve_materia', blank=True, null=True, related_name='materia_Clase_set')
    cve_plan_estudio = models.ForeignKey('MateriaPlanPeriodo', models.DO_NOTHING, db_column='cve_plan_estudio', blank=True, null=True, related_name='planestudio_Clase_set')
    cve_carrera = models.ForeignKey('MateriaPlanPeriodo', models.DO_NOTHING, db_column='cve_carrera', blank=True, null=True)
    cve_especialidad = models.ForeignKey('MateriaPlanPeriodo', models.DO_NOTHING, db_column='cve_especialidad', blank=True, null=True, related_name='especialidad_Clase_set')

    class Meta:
        managed = False
        db_table = 'clase'
        unique_together = (('cve_clase', 'cve_docente'),)

class Docente(models.Model):
    cve_docente = models.CharField(primary_key=True, max_length=10)
    activo = models.BooleanField()
    tipo = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'docente'


class MateriaPlanPeriodo(models.Model):
    cve_periodo = models.OneToOneField('Periodo', models.DO_NOTHING, db_column='cve_periodo', primary_key=True)
    cve_materia = models.ForeignKey('MateriaPlanEstudio', models.DO_NOTHING, db_column='cve_materia', related_name='materia_Mplanperiodo_set')
    cve_plan_estudio = models.ForeignKey('MateriaPlanEstudio', models.DO_NOTHING, db_column='cve_plan_estudio', related_name='plaNestudio_MPlanperiodo_set')
    cve_carrera = models.ForeignKey('MateriaPlanEstudio', models.DO_NOTHING, db_column='cve_carrera', related_name='carrera_MplanPeriodo_set')
    cve_especialidad = models.ForeignKey('MateriaPlanEstudio', models.DO_NOTHING, db_column='cve_especialidad', related_name='especialidad_MPlanPeriodo_set')

    class Meta:
        managed = False
        db_table = 'materia_plan_periodo'
        unique_together = (('cve_periodo', 'cve_materia', 'cve_plan_estudio', 'cve_carrera', 'cve_especialidad'),)


class MateriaPlanEstudio(models.Model):
    cve_materia = models.IntegerField(primary_key=True)
    cve_plan_estudio = models.ForeignKey('PlanEstudio', models.DO_NOTHING, db_column='cve_plan_estudio', related_name='planestudio_MplanEstudio_set')
    cve_carrera = models.ForeignKey('PlanEstudio', models.DO_NOTHING, db_column='cve_carrera', related_name='Carrera_MplanEstudio_set')
    cve_especialidad = models.ForeignKey('PlanEstudio', models.DO_NOTHING, db_column='cve_especialidad', related_name='Especialidad_MplanEstudio_set')
    no_cuatrimestre = models.SmallIntegerField()
    no_unidades = models.IntegerField()
    folio_materia = models.CharField(max_length=20)
    no_horas_semana = models.FloatField(blank=True, null=True)
    integradora = models.BooleanField(blank=True, null=True)
    estadia = models.BooleanField(blank=True, null=True)
    extracurricular = models.BooleanField()
    faltas = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'materia_plan_estudio'
        unique_together = (('cve_materia', 'cve_plan_estudio', 'cve_carrera', 'cve_especialidad'),)


class EspecialidadCarrera(models.Model):
    cve_especialidad = models.SmallIntegerField(primary_key=True)
    cve_carrera = models.SmallIntegerField()
    nombre = models.CharField(max_length=200)
    activo = models.BooleanField()
    abreviatura = models.CharField(max_length=5)
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'especialidad_carrera'
        unique_together = (('cve_especialidad', 'cve_carrera'),)

class PlanEstudio(models.Model):
    cve_plan_estudio = models.SmallIntegerField(primary_key=True)
    cve_carrera = models.ForeignKey(EspecialidadCarrera, models.DO_NOTHING, db_column='cve_carrera', related_name='carrera_planEstudio_set')
    cve_especialidad = models.ForeignKey(EspecialidadCarrera, models.DO_NOTHING, db_column='cve_especialidad')
    nombre = models.CharField(max_length=15)
    fecha_inicio = models.DateTimeField()
    tipo = models.CharField(max_length=1)
    nomenclatura = models.CharField(max_length=5)
    activo = models.BooleanField(blank=True, null=True)
    punto_de_pase = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_estudio'
        unique_together = (('cve_plan_estudio', 'cve_carrera', 'cve_especialidad'),)

class AlumnoClase(models.Model):
    matricula = models.OneToOneField(Alumno, models.DO_NOTHING, db_column='matricula', primary_key=True)
    cve_clase = models.ForeignKey('Clase', models.DO_NOTHING, db_column='cve_clase')
    cve_docente = models.ForeignKey('Clase', models.DO_NOTHING, db_column='cve_docente', related_name='docente_AlumnoClase_set')
    cve_status = models.SmallIntegerField(blank=True, null=True)
    calificacion_final = models.FloatField()

    class Meta:
        managed = False
        db_table = 'alumno_clase'
        unique_together = (('matricula', 'cve_docente', 'cve_clase'),)
