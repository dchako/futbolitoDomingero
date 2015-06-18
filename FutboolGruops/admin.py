from django.contrib import admin
from .models import User, Eventos, Equipos, Grupos, Jugador, Invitacion
from .models import Partidos

admin.site.register(User)
admin.site.register(Eventos)
admin.site.register(Equipos)
admin.site.register(Grupos)
admin.site.register(Jugador)
admin.site.register(Invitacion)
admin.site.register(Partidos)