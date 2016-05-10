# -*- coding: utf-8 -*-
from .models import Eventos, Equipos, Grupos, User, Jugador, Invitacion
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'status', 'avatar', 'first_name',
                 'last_name')


class UserSerializer_2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class GruposSerializer(serializers.HyperlinkedModelSerializer):
    usuarioCreador = UserSerializer_2(read_only=True)

    class Meta:
        model = Grupos
        fields = ('nombreDelGrupo', 'fechaCreacion', 'usuarioCreador')


class EventosSerializer(serializers.HyperlinkedModelSerializer):
    #usuarioCreador = UserSerializer_2(read_only=True)
    nombreDGrupos = GruposSerializer(read_only=True)

    class Meta:
        model = Eventos
        fields = ('pk', 'nombreDGrupos',
                  #'usuarioCreador',
                 'dias_horas',
                 'lugar', 'cancha_5', 'cancha_7', 'cancha_11')


class EquiposSerializer(serializers.HyperlinkedModelSerializer):
    nombreDelGrupos = EventosSerializer(read_only=True)

    class Meta:
        model = Equipos
        fields = ('nombreDelEquipo', 'nombreDelGrupos', 'local_visitante')


class JugadoresSerializer(serializers.HyperlinkedModelSerializer):
    usuario = UserSerializer(read_only=True)
    eventos = EventosSerializer(read_only=True)
    equipo = EquiposSerializer(read_only=True)

    class Meta:
        model = Jugador
        fields = ('eventos', 'usuario', 'equipo', 'asistencia')


class InvitacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invitacion
        fields = ('evento', 'usuario_invitado', 'dias_invitacion', 'estado')
