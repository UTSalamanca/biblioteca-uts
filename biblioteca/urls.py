from django.contrib import admin
from django.urls import path, include, re_path
from inicio.views import index_inicio
from django.contrib.auth.decorators import login_required
# from login.views import logoutUser
from login.views import login_view
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls, name = 'panel'),
    # Ruta de logeo
    path('login/', include('login.urls')),
    path('', login_view),
    # path('logout/', login_required(logout_view), name = 'logout'),
    # Rutas app Inicio
    path('inicio/', include('inicio.urls')),
    # Rutas app Acervo
    path('acervo/', include('almacen.urls')),
    # Rutas app estadías
    path('estadias/', include('estadias.urls')),
    # aplicación de sesión
    path('session-security/', include('session_security.urls')),
    # Aplicación de catalogo
    path('catalogo/', include('catalogo.urls')),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
