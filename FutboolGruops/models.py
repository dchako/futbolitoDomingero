from django.db import models
from datetime import datetime
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin)


#custom usuario
class UserManager(BaseUserManager):

        def _create_user(
       self, username, email, password, is_staff, is_superuser, **extra_fields):
            if not email:
                return ValueError('El email es Obligatorio')
            email = self.normalize_email(email)
            user = self.model(
            username=username, email=email, is_active=True, is_staff=is_staff,
                is_superuser=is_superuser, **extra_fields)
            user.set_password(password)
            user.save(using=self.db)
            return user

        def create_user(self, username, email, password=None, **extra_fields):
            return self._create_user(
                       username, email, password, False, False, **extra_fields)

        def create_superuser(self, username, email, password, **extra_fields):
            return self._create_user(
                        username, email, password, True, True, **extra_fields)


#es la tabla de jugadores
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.URLField()
    status = models.BooleanField(default=False)

    objects = UserManager()

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return  self.username

    def get_username(self):
        return  self.username

    def get_short_name(self):
        return  self.first_name

#tablas super locas
#tabla grupete


class Grupos(models.Model):
    nombreDelGrupo = models.CharField(max_length=30, unique=True)
    fechaCreacion = models.DateTimeField(default=datetime.now(), blank=True)
    usuarioCreador = models.ForeignKey('User')

    def __unicode__(self):
        return self.nombreDelGrupo

#tabla intermedia
#tabla equipete


class Equipos(models.Model):

    nombreDelEquipo = models.CharField(max_length=30)
    nombreDelGrupos = models.ForeignKey('Eventos', )
    local_visitante = models.BooleanField(default=False, )

    class Meta:
        unique_together = (("nombreDelGrupos", "local_visitante"),)

    def __unicode__(self):
        return (self.nombreDelEquipo)
#tabla eventos


class Eventos(models.Model):

    nombreDGrupos = models.ForeignKey('Grupos')
    usuarioCreador = models.ForeignKey('User')
    dias_horas = models.DateTimeField(default=datetime.now(), blank=True)
    lugar = models.CharField(max_length=30)
    cancha_5 = models.BooleanField(default=True)
    cancha_7 = models.BooleanField(default=False)
    cancha_11 = models.BooleanField(default=False)

    def __unicode__(self):
        return (self.lugar)


class Jugador(models.Model):

    eventos = models.ForeignKey('Eventos',)
    usuario = models.ForeignKey('User', )
    equipo = models.ForeignKey('Equipos',)
    asistencia = models.BooleanField(default=False)

    class Meta:
        unique_together = (("eventos", "usuario", "equipo"),)


class Invitacion(models.Model):

    evento = models.ForeignKey('Eventos', )
    usuario_invitado = models.ForeignKey('User',)
    dias_invitacion = models.DateTimeField(default=datetime.now(), blank=True)
    estado = models.BooleanField(default=False)

    class Meta:
        unique_together = (("evento", "usuario_invitado",),)

    def __unicode__(self):
        return (self.usuario_invitado.username)