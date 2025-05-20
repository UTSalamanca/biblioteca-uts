from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'estadias'

urlpatterns = [
    path('estadias_registro/',login_required(views.estadias_registro), name='estadias_registro'),
    path('get_alumno/', login_required(views.get_alumno), name='get_alumno'),
    path('insert_consult/', login_required(views.insert_consult), name='insert_consult'),
    path('view_report/<report_rute>', login_required(views.view_report), name='view_report'),
    path('view_report/<report_rute>', login_required(views.servir_pdf), name='servir_pdf'),
    path('proyectos/',login_required(views.index_proyectos), name='proyectos'),
]