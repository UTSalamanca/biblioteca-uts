from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from sistema.models import UsuarioAcceso

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterUserForm(UserCreationForm):
    login = forms.CharField(max_length=9, help_text='Matricula')
    email = forms.EmailField(max_length=150, help_text='Correo institucional')
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
        strip=False, # this help text contains list of hints
    )
    password2 = forms.CharField(
        label=_("Confirmar Contraseña"),
        widget=forms.PasswordInput,
        strip=False, # this help text contains list of hints
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@utsalamanca.edu.mx'):
            raise ValidationError('El correo electrónico debe ser de @utsalamanca.edu.mx')
        return email

    class Meta:
        model = UsuarioAcceso
        fields = ('login', 'email', 'password1', 'password2')
        exclude = ['cve_persona',]

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.login = self.cleaned_data['login']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioAcceso
        fields = ('avatar',)

    avatar = forms.ImageField(required=False)
