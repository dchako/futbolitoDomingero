from django.db import models
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin)

#custom usuario
class UserManager(BaseUserManager):

	def _create_user(self, username, email,password,is_staff,is_superuser, **extra_fields):
		if not email:
			return ValueError('El email es Obligatorio')
		email = self.normalize_email(email)
		user = self.model(username = username, email= email, is_active = True, is_staff = is_staff, 
			is_superuser= is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self, username, email, password = None, **extra_fields):
		return self._create_user(username, email, password, False, False, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		return self._create_user(username, email, password, True, True, **extra_fields)

#es la tabla de jugadores
class User(AbstractBaseUser, PermissionsMixin):
       
    username = models.CharField(max_length=30, unique = True)
    email = models.EmailField(max_length=50, unique = True)
    first_name = models.CharField( max_length=30, blank=True, null=True)
    last_name = models.CharField( max_length=30, blank=True, null=True)
    avatar = models.URLField()
    status = models.BooleanField(default=False)

#    equipo = models.ForeignKey(Equipos)

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
"""
#tablas super locas
class Grupos(models.Model):
    username = models.CharField(max_length=30, unique = True)
    members = models.ManyToManyField(User, through ='Membership')

    def __unicode__(self):
    	return self.name


class Membership(models.Model):
	jugador = models.ForeignKey(User)
	grupo =  models.ForeignKey(Grupos)
	dias_horas = models.DateField()
	lugar = models.CharField(max_length=30, unique = True)
	asistencia = models.BooleanField(default=False)


class Equipos(models.Model):

	nombre = models.ForeignKey(Grupos)
	visitante_local = models.BooleanField(default=False)
"""
