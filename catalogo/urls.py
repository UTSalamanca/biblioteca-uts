from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('catalago', login_required(views.catalogo), name='catalago'),
    path('prestamo_registro/', login_required(views.prestamo_registro), name='prestamo_registro'),
    path('prestamos_View/', login_required(views.prestamos_View), name='prestamos_View'),
    path('cargar_portada/', login_required(views.cargar_portada), name='cargar_portada'),
    path('search_book/', login_required(views.search_book), name='search_book'),
    path('edit_portada/', login_required(views.edit_portada), name='edit_portada'),
    path('view_book/', login_required(views.view_book), name='view_book'),
    path('book_delivered/<str:cve>/<str:entrega>', login_required(views.book_delivered), name='book_delivered'),
    path('renew_again/<str:cve>/<int:cant>/<str:entrega>', login_required(views.renew_again), name='renew_again'),
    path('cant_for_search/', login_required(views.cant_for_search), name='cant_for_search'),
    path('prestamos_usuario/', login_required(views.prestamos_usuario), name='prestamos_usuario'),
    path('get_personas_p/', login_required(views.get_alumno), name='get_personas_p'),
]