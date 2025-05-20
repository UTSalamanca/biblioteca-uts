from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', login_required(views.index_inicio), name = 'inicio'),
    # Generación de reporte xlsx
    path('report/<int:periodo>', login_required(views.report), name='report'),
    path('get_periodo/', login_required(views.get_periodo), name='get_periodo'),
]