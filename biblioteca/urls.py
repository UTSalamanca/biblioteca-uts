from django.contrib import admin
from django.urls import path, include, re_path
from almacen.views import index_acervo as acervo
from almacen.views import acervo_registro, delete_acervo, edit_register, edit_acervo, temp_formato_add
from inicio.views import index_inicio as inicio, report
from estadias.views import index_proyectos as proyectos
from django.contrib.auth.decorators import login_required
from login.views import logoutUser
from estadias.views import estadias_registro
from estadias.views import view_report, servir_pdf, get_alumno, insert_consult
from usuario.views import login_view
from catalogo.views import catalago_View, prestamos_View, prestamo_registro, cargar_portada, search_book, edit_portada, view_book, book_delivered, get_book_for_person, renew_again, cant_for_search
from catalogo.views import get_alumno as get_personas_p

from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls, name = 'panel'),
    path('acervo/', login_required(acervo), name = 'acervo'),
    path('temp_formato_add/', login_required(temp_formato_add), name = 'temp_formato_add'),
    path('', login_required(inicio), name = 'inicio'),
    # path('accounts/login/', Login.as_view(), name = 'login'),
    path('accounts/login/', login_view, name = 'login'),
    path('logout/', login_required(logoutUser), name = 'logout'),

    path('proyectos/',login_required(proyectos),name='proyectos'),
    # Rutas app Acervo
    path('acervo_registro/', login_required(acervo_registro), name='acervo_registro'),
    path('delete_acervo/<col>', login_required(delete_acervo), name='delete_acervo'),
    path('edit_register/<col>', login_required(edit_register), name='edit_register'),
    path('edit_acervo/', login_required(edit_acervo), name='edit_acervo'),
    # Rutas app estadías
    path('estadias_registro/',login_required(estadias_registro)),
    path('get_alumno/', login_required(get_alumno), name='get_alumno'),
    path('insert_consult/', login_required(insert_consult), name='insert_consult'),
    path('view_report/<report_rute>', login_required(view_report), name='view_report'),
    path('view_report/<report_rute>', login_required(servir_pdf), name='servir_pdf'),
    # aplicación de sesión
    path('session-security/', include('session_security.urls')),
    # Aplicación de catalogo
    path('catalago_View', login_required(catalago_View), name='catalago_View'),
    path('prestamo_registro/', login_required(prestamo_registro), name='prestamo_registro'),
    path('prestamos_View/', login_required(prestamos_View), name='prestamos_View'),
    path('cargar_portada/', login_required(cargar_portada), name='cargar_portada'),
    path('search_book/', login_required(search_book), name='search_book'),
    path('edit_portada/', login_required(edit_portada), name='edit_portada'),
    path('view_book/', login_required(view_book), name='view_book'),
    path('book_delivered/<str:cve>/<str:entrega>', login_required(book_delivered), name='book_delivered'),
    path('renew_again/<str:cve>/<int:cant>/<str:entrega>', login_required(renew_again), name='renew_again'),
    path('cant_for_search/', login_required(cant_for_search), name='cant_for_search'),
    path('get_book_for_person/', login_required(get_book_for_person), name='get_book_for_person'),
    path('get_personas_p/', login_required(get_personas_p), name='get_personas_p'),
    # Generación de reporte xlsx
    path('report/', login_required(report), name='report'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
