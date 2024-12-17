from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from sito.models import Persona
from static.helpers import dd

# Create your models here.

class UsuarioManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, login, password=None, **extra_fields):
        if not login:
            raise ValueError(_('El campo nombre de usuario es requerido.'))
        if not email:
            raise ValueError(_('El campo email es requerido.'))

        user = self.model(email=self.normalize_email(email), login=login, **extra_fields)
        user.cve_persona = 2409
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, login, password, **extra_fields):
        user = self.create_user(email, login, password)
        user.activo = True
        user.staff = True
        user.superuser = True
        user.save()
        return user

class UsuarioAcceso(AbstractBaseUser, PermissionsMixin):
    cve_persona = models.IntegerField(primary_key=True, unique=True)
    login = models.CharField('Nombre de usuario', max_length=10, unique=True)
    password = models.CharField(max_length=128)
    activo = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True, editable=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    avatar = models.ImageField(default='avatar/default.png', upload_to='avatar', null=True, blank=True)

    # @property
    # def persona(self):
    #     return Persona.objects.get(cve_persona=self.cve_persona)

    object = UsuarioManager()
    objects = models.Manager()

    username = None

    USERNAME_FIELD = 'login'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.login}'

    # def has_perm(self,perm,obj = None):
    #     return self.is_superuser

    # def has_module_perms(self,app_label):
    #     return self.is_superuser

    @property
    def is_active(self):
        return self.activo

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    class Meta:
        # managed = False
        # abstract = True
        db_table = 'sistema_usuario'
        verbose_name = 'Acceso Usuario'
        verbose_name_plural = 'Acceso Usuarios'