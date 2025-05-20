from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from sistema.models import UsuarioAcceso

class UsuarioAccesoChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UsuarioAcceso
        fields = ('login', 'password', 'email', 'activo', 'staff', 'superuser')