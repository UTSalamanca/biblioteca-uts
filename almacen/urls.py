from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'acervo'

urlpatterns = [
    path('acervo/', login_required(views.index_acervo), name = 'acervo'),
    path('temp_formato_add/', login_required(views.temp_formato_add), name = 'temp_formato_add'),
    path('acervo_registro/', login_required(views.acervo_registro), name='acervo_registro'),
    path('delete_acervo/<str:col>', login_required(views.delete_acervo), name='delete_acervo'),
    path('edit_register/<col>', login_required(views.edit_register), name='edit_register'),
    path('edit_acervo/', login_required(views.edit_acervo), name='edit_acervo'),
    path('get_match/', login_required(views.get_match), name='get_match'),
    path('get_register/', login_required(views.get_register), name='get_register'),
]