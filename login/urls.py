from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'usuario'

urlpatterns = [
    # Generación de reporte xlsx
    path('verify_account/', views.verify_account_view, name='verify_account'),
    # path('login/', TemplateView.as_view(template_name='login/base.html'), name='login'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]