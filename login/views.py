from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from .forms import formularyLogin
from sistema.models import UsuarioAcceso
from django.contrib import messages
# from django.contrib.auth.models import check_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# class Login(FormView):
#     print('entraaa Login de login')
#     template_name = 'index_login.html'
#     form_class = formularyLogin
#     success_url = reverse_lazy('inicio')
# 
#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             messages.add_message(request, messages.ERROR, 'Por favor introduzca un nombre de usuario y contraseña correctos.')
#             return super(Login,self).dispatch(request, *args, **kwargs)
# 
# 
#     def form_valid(self, form):
#         login(self.request,form.get_user())
#         return super(Login,self).form_valid(form)

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')
