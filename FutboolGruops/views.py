from django.shortcuts import render_to_response, render, redirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Eventos, Equipos, Grupos, User, Jugador, Invitacion
from .models import Partidos
from django.http import HttpResponse
import json
from django.http import Http404
from dateutil.rrule import *
from datetime import datetime
from dateutil.tz import tzutc
#desde aca todo nuevo
from social.apps.django_app.utils import load_strategy, load_backend, strategy
#from social.apps.django_app.utils import psa
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
#from django.utils.six.moves import http_client
from social.apps.django_app.views import _do_login
from rest_framework import viewsets
from .serializers import UserSerializer, JugadoresSerializer
from .serializers import EventosSerializer, EquiposSerializer
from .serializers import GruposSerializer, InvitacionSerializer
from rest_framework.filters import DjangoFilterBackend
#from django_filters import filters
# Create your views here.
import pdb


@login_required(login_url='/login')
def home(request, id):
    if request.user.status:
        #traigo con el usuario todos los  evento del usuario!
        eventoDadmins = Jugador.objects.filter(usuario=request.user.id)
        if id == '0':
            todos_los_usuarios = Jugador.objects.filter(eventos=eventoDadmins[0].eventos.id)
            eventoDadmin = get_object_or_404(Jugador,eventos=eventoDadmins[0].eventos.id,usuario=request.user.id).eventos
            partido = Partidos.objects.order_by('-fechaCreacion').filter(eventos=eventoDadmins[0].eventos.id,)
        else:
            #ACA EXPLOTA CUANDO EL ID Y EL USUARIO NO PERTENECE AL ID
            eventoDadmin = get_object_or_404(Jugador, eventos=int(id), usuario=request.user.id).eventos
            partido = Partidos.objects.order_by('-fechaCreacion').filter(eventos=int(id))
            #traigo con un evento todo los jugadores de ese evento
            todos_los_usuarios = Jugador.objects.filter(eventos=eventoDadmin.id)
        cantidad = todos_los_usuarios.count
        asis = Jugador.objects.filter(eventos=eventoDadmin.id, asistencia=True)
        asisten = asis.count
        Todos_los_equipos = Equipos.objects.filter(nombreDelGrupos=eventoDadmin.id)
        ju_v = Jugador.objects.filter(eventos=eventoDadmin.id, equipo=Todos_los_equipos[0].id)
        ju_l = Jugador.objects.filter(eventos=eventoDadmin.id, equipo=Todos_los_equipos[1].id)
        l, L = (list(ju_v), list(ju_l))
        if len(l) > len(L):
            L = L + [None for x in range(len(l) - len(L))]
        else:
            l = l + [None for x in range(len(L) - len(l))]
        jugadores = [{'j1':L[x], 'j2':l[x]} for x in range(len(L))]
        #Aca el calculo recurrente
        dias_recurrente = rrule(DAILY, byweekday=(1, 3), dtstart=eventoDadmin.dias_horas)
        dia_cercano = dias_recurrente.after(dt=datetime.now(tzutc()), inc=True)
        cant_p = len(partido)
        if cant_p > 1:
            partido_proximo = partido[0]
            partido_anterior = partido[1]
        else:
            partido_proximo = partido[0]
            partido_anterior = partido[0]

        if  datetime.now(tzutc()) > partido_proximo.fechaCreacion:
            cargar_goles = 1
            partido_proximo.fechaCreacion = dia_cercano
            partido_proximo.save()
        else:
            cargar_goles = 0
        #tengo ...
        obj_invit = Invitacion.objects.filter(usuario_invitado=request.user.id, estado=False,)
        cant = obj_invit.count
        ctx = {'todos_los_usuarios': todos_los_usuarios,
            'nombreDelGrupos': eventoDadmins,
            'nombreDelGrupo': eventoDadmin,
            'Todos_los_equipos': Todos_los_equipos,
            'jugadores': jugadores,
            'equipo_local': Todos_los_equipos.get(local_visitante=True).nombreDelEquipo,
            'equipo_visitante': Todos_los_equipos.get(local_visitante=False).nombreDelEquipo,
            'asisten': asisten,
            'cantidad': cantidad,
            'cant': cant,
            'gol_visitante': partido_anterior.visitante,
            'gol_local': partido_anterior.local,
            'dia_cercano': dia_cercano,
            'cargar_goles': cargar_goles,
            'id_evento': partido_anterior.id,
            }
        return render(request, 'home.html', ctx)
    else:
        return redirect('registrar')

def home_2(request):
    return redirect('login')

def error(request):
    return render_to_response('error.html',
                                context_instance=RequestContext(request))


@login_required(login_url='/login')
def configurar(request, id):
    #traido el evento por id
    evento_jugad = get_object_or_404(Jugador,
                     eventos=id, usuario=request.user.id).eventos
    #traigo el equipo por id
    equipo_l = get_object_or_404(Equipos,
                     nombreDelGrupos=id, local_visitante=False)
    equipo_v = get_object_or_404(Equipos,
                     nombreDelGrupos=id, local_visitante=True)
    if request.POST:
        #Aca de realiza el update
        nombre_Equipo = request.POST["Equipos-nombreDelEquipo"]
        nombre_Equipo_v = request.POST["Equipo_visitante-nombreDelEquipo"]
        #instancio y cargo con el request y los datos a updatear
        a1 = ExtraDataForm_grupos(
                             request.POST, instance=evento_jugad.nombreDGrupos)
        b1 = ExtraDataForm_Equipos(
                    request.POST, instance=equipo_l, prefix="Equipos")
        c1 = ExtraDataForm_Equipos(
                    request.POST, instance=equipo_v, prefix="Equipo_visitante")
        d1 = ExtraDataForm_Membership(
                                           request.POST, instance=evento_jugad)
        if(nombre_Equipo != nombre_Equipo_v):
            #aca valido
            equi_v = c1.is_valid()
            grup = a1.is_valid()
            equi = b1.is_valid()
            member = d1.is_valid()
            if (equi and grup and member and equi_v):
                a1.save()
                b1.save()
                c1.save()
                d1.save()
                ids = id
                return redirect('/', id=ids)
            else:
                #Aca se se manda los errores o las no validacion
                print("entro aca porque tiener errores en el forms")
                mensaje = ""
                ctx = {
                'mensajeDeError': mensaje,
                'error_diaDeJuegoYhoras': d1['dias_horas'].errors.as_text(),
                'error_lugar': d1['lugar'].errors.as_text(),
                'error_nombreDelGrupo': a1['nombreDelGrupo'].errors.as_text(),
                'error_nombreDeEquipoLocal': (
                                    b1['nombreDelEquipo'].errors.as_text()),
                'error_nombreDelEquipoVisitante': (
                                      c1['nombreDelEquipo'].errors.as_text()),
                'form_grupos': a1,
                'form_equipos': b1,
                'form_equipos_v': c1,
                'form_membership': d1,
                'form': ExtraDataForm(request.POST),
                       }
                return render(request, 'registrar.html', ctx)
        else:
            #si los grupo son repetidos son repetidos
            mensaje = "los equipos deven ser diferentes"
            ctx = {
                'mensajeDeError': mensaje,
                'error_diaDeJuegoYhoras': d1['dias_horas'].errors.as_text(),
                'error_lugar': d1['lugar'].errors.as_text(),
                'error_nombreDelGrupo': a1['nombreDelGrupo'].errors.as_text(),
                'error_nombreDeEquipoLocal': (
                                    b1['nombreDelEquipo'].errors.as_text()),
                'error_nombreDelEquipoVisitante': (
                                      c1['nombreDelEquipo'].errors.as_text()),
                'form_grupos': a1,
                'form_equipos': b1,
                'form_equipos_v': c1,
                'form_membership': d1,
                'form': ExtraDataForm(request.POST),
                       }
            return render(request, 'registrar.html', ctx)
    #NO ES POST-- carga los datos a los formularios por id
    mensaje = " "
    ctx = {
        'form_grupos': ExtraDataForm_grupos(
                                         instance=evento_jugad.nombreDGrupos),
        'form_equipos': ExtraDataForm_Equipos(
                                        instance=equipo_l, prefix="Equipos"),
        'form_equipos_v': ExtraDataForm_Equipos(
                                 instance=equipo_v, prefix='Equipo_visitante'),
        'form_membership': ExtraDataForm_Membership(instance=evento_jugad),
        'form': ExtraDataForm(request.POST),
        'mensajeDeError': mensaje
                  }
    return render(request, 'registrar.html', ctx)


@login_required(login_url='/login')
def invitacion(request):
    obj_invit = Invitacion.objects.filter(
            usuario_invitado=request.user.id,
            estado=False,
            )
    ctx = {'obj_invit': obj_invit,
            }
    return render(request, 'invitacion.html', ctx)


def asistencia_ajax(request):
    if request.is_ajax():
        nombre = request.GET['nombre']
        grupete = request.GET['grupo']
        accionista = request.GET['accion']
        data = {}
        try:
            obj_usuario = User.objects.get(username=nombre)
            grupe = Grupos.objects.get(nombreDelGrupo=grupete)
            obj_evento = Eventos.objects.get(nombreDGrupos=grupe)
            g = Jugador.objects.get(
                        usuario=obj_usuario, eventos=obj_evento.id)
            if(accionista == '1'):
                g.asistencia = True
            else:
                g.asistencia = False
            g.save()
            data['code'] = 'OK'
        except e:
            print(e)
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


def cargar_goles(request):
    if request.is_ajax():
        fecha_proximo = request.GET['fecha_proximo']
        id_evento = request.GET['id_evento']
        gol_v = request.GET['gol_v']
        gol_l = request.GET['gol_l']
        data = {}
        try:
            partido_anterior = Partidos.objects.get(id=id_evento)
        except e:
            partido_anterior = Partidos.objects.create(
                            eventos=id_evento,
                            )
        try:
            partido_anterior.local = int(gol_l)
            partido_anterior.visitante = int(gol_v)
            partido_anterior.save()
            data['code'] = 'OK'
        except e:
            print(e)
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


def invitacion_ajax(request):
    if request.is_ajax():
        ids = request.GET['id']
        accionista = request.GET['accion']
        data = {}
        try:
            obj_invit = Invitacion.objects.get(id=ids)
            equipos = Equipos.objects.filter(nombreDelGrupos=obj_invit)
            if(accionista == '1'):
                jug = Jugador.objects.create(
                             eventos=obj_invit.evento,
                             usuario=obj_invit.usuario_invitado,
                             equipo=equipos[0],
                            )
                jug.save()
                obj_invit.estado = True
            else:
                obj_invit.estado = True
            obj_invit.save()
            data['code'] = 'OK'
        except e:
            print(e)
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


def cambioDeEquipo_ajax(request):
    if request.is_ajax():
        nombre = request.GET['nombre']
        grupete = request.GET['grupo']
        data = {}
        try:
            obj_usuario = User.objects.get(username=nombre)
            grupe = Grupos.objects.get(
                    nombreDelGrupo=grupete,
                    )
            obj_evento = Eventos.objects.get(
                            nombreDGrupos=grupe,)
            obj_equipos = Equipos.objects.filter(
                            nombreDelGrupos=obj_evento.id)
            g = Jugador.objects.get(
                        usuario=obj_usuario,
                         eventos=obj_evento.id,)
            if(g.equipo.id == obj_equipos[0].id):
                g.equipo = obj_equipos[1]
            else:
                g.equipo = obj_equipos[0]
            g.save()
            data['code'] = 'OK'
        except e:
            print(e)
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


def invitar_ajax(request):
    if request.is_ajax():
        nombre = request.GET['usuario_invitado']
        grupete = request.GET['grupete']
        data = {}
        try:
            obj_usuario_invitado = User.objects.get(username=nombre)
            obj_usuario = User.objects.get(username=request.user)
            grupe = Grupos.objects.get(
                    nombreDelGrupo=grupete, usuarioCreador=obj_usuario)
            obj_evento = Eventos.objects.get(
                            usuarioCreador=obj_usuario, nombreDGrupos=grupe)
            invitacion = Invitacion.objects.create(
                evento=obj_evento,
                usuario_invitado=obj_usuario_invitado,
                )
            invitacion.save()
            data['code'] = 'OK'
        except e:
            print(e)
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


@login_required(login_url='/login')
def invitar(request, id):
    admineventos = Jugador.objects.filter(usuario=request.user.id)
    eventoDadmin = Eventos.objects.filter(usuarioCreador=request.user.id)
    if id == '0':
        eventoDadmins = get_object_or_404(Jugador,
                                eventos=admineventos[0].eventos.id,
                                usuario=request.user.id).eventos
    else:
        eventoDadmins = get_object_or_404(Jugador,
                                            eventos=id,
                                            usuario=request.user.id).eventos
    mensaje = ""
    if request.POST:
        try:
            usuario = User.objects.get(username=request.POST["username"])
            grupoAdmin = Eventos.objects.filter(usuarioCreador=usuario)
            EventoAdmin = Jugador.objects.filter(eventos=grupoAdmin[0].id)
        except User.DoesNotExist:
            mensaje = "No Existe el usuario"
            ctx = {
                'form': ExtraDataForm(request.POST),
                'nombreDelGruposs': eventoDadmin,
                'nombreDelGrupo': eventoDadmins.nombreDGrupos,
                'error': mensaje,
                  }
            return render(request, 'invitar.html', ctx,
                                    context_instance=RequestContext(request))
        ctx = {
            'nombre_jugador': usuario,
            'nombreDelGrupos': grupoAdmin[0].nombreDGrupos,
            'nombreDelGrupo': eventoDadmins.nombreDGrupos,
            'equipo_local': EventoAdmin[0].equipo,
            'nombreDelGruposs': eventoDadmin,
            'error': mensaje,
            'form': ExtraDataForm(request.POST),
            }
        return render(request, 'invitar.html', ctx,
                                    context_instance=RequestContext(request))
    ctx = {
        'form': ExtraDataForm(request.POST),
        'error': mensaje,
        'nombreDelGrupo': eventoDadmins.nombreDGrupos,
        'nombreDelGruposs': eventoDadmin,
        }
    return render_to_response('invitar.html', ctx,
                                    context_instance=RequestContext(request))


@login_required(login_url='/login')
def estrategias(request, id):
        #traigo con el usuario todos los  evento del usuario!
        eventoDadmins = Jugador.objects.filter(usuario=request.user.id)
        if id == '0':
            eventoDadmin = get_object_or_404(Jugador,
                                        eventos=eventoDadmins[0].eventos.id,
                                        usuario=request.user.id).eventos
        else:
            #ACA EXPLOTA CUANDO EL ID Y EL USUARIO NO PERTENECE AL ID
            eventoDadmin = get_object_or_404(Jugador,
                                           eventos=id,
                                           usuario=request.user.id).eventos
        obj_invit = Invitacion.objects.filter(
                    usuario_invitado=request.user.id,
                    estado=False,)
        cant = obj_invit.count
        ctx = {
            'nombreDelGrupos': eventoDadmins,
            'nombreDelGrupo': eventoDadmin.nombreDGrupos,
            'cant': cant,
            }
        return render(request, 'estrategias.html', ctx)


def login(request):
    return render_to_response('login.html',
                                context_instance=RequestContext(request))


class ExtraDataView(View):

        template_name = 'registrar.html'

        def get(self, request, *args, **kwargs):
            mensaje = ""
            ctx = {
        'form_grupos': ExtraDataForm_grupos(prefix="Grupos"),
        'form_equipos': ExtraDataForm_Equipos(prefix='Equipos'),
        'form_equipos_v': ExtraDataForm_Equipos(prefix='Equipo_visitante'),
        'form_membership': ExtraDataForm_Membership(prefix="Membership"),
        'form': ExtraDataForm(request.POST),
        'mensajeDeError': mensaje
                  }
            return render(request, self.template_name, ctx)

        def post(self, request, *args, **kwargs):

            #aca cargo los datos al formulario y valido
            form = ExtraDataForm(request.POST)
            form_grupos = ExtraDataForm_grupos(request.POST, prefix='Grupos')
            form_membership = ExtraDataForm_Membership(request.POST,
                              prefix="Membership")
            form_equipos = ExtraDataForm_Equipos(request.POST,
                              prefix="Equipos")
            form_equipos_v = ExtraDataForm_Equipos(request.POST,
                              prefix='Equipo_visitante')

            #aca valido
            equi_v = form_equipos_v.is_valid()
            grup = form_grupos.is_valid()
            equi = form_equipos.is_valid()
            member = form_membership.is_valid()

            if (equi and grup and member and equi_v):
                    #aca saco los datos
                    nombre_Equipo = (
                            form_equipos.cleaned_data["nombreDelEquipo"])
                    nombre_Equipo_v = (
                        form_equipos_v.cleaned_data["nombreDelEquipo"])
                    #print(nombre_Equipo)
                    #print(nombre_Equipo_v)
                    if(nombre_Equipo != nombre_Equipo_v):
                        if form.is_valid():
                            request.user.username = request.POST['username']
                        else:
                            request.user.username = request.user.username
                        request.user.status = True
                        #creo el grupo
                        grupos = Grupos.objects.create(
                     nombreDelGrupo=form_grupos.cleaned_data["nombreDelGrupo"],
                     usuarioCreador=User.objects.get(id=request.user.id))
                        grupos.save()
                        request.user.save()
                         #creo el evento
                        evento = Eventos.objects.create(
                          usuarioCreador=User.objects.get(id=request.user.id),
                          nombreDGrupos=grupos,
                      dias_horas=form_membership.cleaned_data.get('dias_horas'),
                          lugar=form_membership.cleaned_data.get('lugar'),
                          cancha_5=form_membership.cleaned_data.get('cancha_5'),
                          cancha_7=form_membership.cleaned_data.get('cancha_7'),
                        cancha_11=form_membership.cleaned_data.get('cancha_11'),
                          )
                        evento.save()
                        #creo equipo local y visitante
                        equipo_l = Equipos.objects.create(
                            nombreDelEquipo=nombre_Equipo,
                            nombreDelGrupos=evento,
                            local_visitante=True,
                            )
                        equipo_v = Equipos.objects.create(
                            nombreDelEquipo=nombre_Equipo_v,
                            nombreDelGrupos=evento,
                            )
                        #guardamos equipo y usuario
                        equipo_l.save()
                        equipo_v.save()
                        jug = Jugador.objects.create(
                             eventos=evento,
                             usuario=User.objects.get(id=request.user.id),
                             equipo=equipo_l,
                            )
                        #creo el registro de partidos
                        partidos = Partidos.objects.create(
                            eventos=evento,
                  fechaCreacion=form_membership.cleaned_data.get('dias_horas'),
                            )
                        partidos.save()
                        jug.save()
                        return redirect('/0')
                    else:
                        mensaje = "los equipos deven ser diferentes"
                        ctx = {
            'mensajeDeError': mensaje,
            'error_username': form['username'].errors.as_text(),
     'error_diaDeJuegoYhoras': form_membership['dias_horas'].errors.as_text(),
            'error_lugar': form_membership['lugar'].errors.as_text(),
        'error_nombreDelGrupo': form_grupos['nombreDelGrupo'].errors.as_text(),
 'error_nombreDeEquipoLocal': form_equipos['nombreDelEquipo'].errors.as_text(),
 'error_nombreDelEquipoVisitante':
             form_equipos_v['nombreDelEquipo'].errors.as_text(),
               'form_grupos': ExtraDataForm_grupos(request.POST,
                   prefix="Grupos"),
        'form_equipos': ExtraDataForm_Equipos(request.POST,
            prefix="Equipos"),
        'form_equipos_v': ExtraDataForm_Equipos(request.POST,
                            prefix="Equipo_visitante"),
        'form_membership': ExtraDataForm_Membership(request.POST,
            prefix="Membership"),
        'form': ExtraDataForm(request.POST),
                       }
                        return render(request, self.template_name, ctx)
            else:
                print("entro aca porque tiener errores en el forms")
                mensaje = ""
                ctx = {
                    'mensajeDeError': mensaje,
            'error_username': form['username'].errors.as_text(),
     'error_diaDeJuegoYhoras': form_membership['dias_horas'].errors.as_text(),
            'error_lugar': form_membership['lugar'].errors.as_text(),
        'error_nombreDelGrupo': form_grupos['nombreDelGrupo'].errors.as_text(),
 'error_nombreDeEquipoLocal': form_equipos['nombreDelEquipo'].errors.as_text(),
 'error_nombreDelEquipoVisitante':
             form_equipos_v['nombreDelEquipo'].errors.as_text(),
               'form_grupos': ExtraDataForm_grupos(request.POST,
                   prefix="Grupos"),
        'form_equipos': ExtraDataForm_Equipos(request.POST,
            prefix="Equipos"),
        'form_equipos_v': ExtraDataForm_Equipos(request.POST,
                            prefix="Equipo_visitante"),
        'form_membership': ExtraDataForm_Membership(request.POST,
            prefix="Membership"),
        'form': ExtraDataForm(request.POST),
                       }
                return render(request, self.template_name, ctx)

#add the following to views.py


@strategy()
#@psa('social:complete')
def auth_by_token(request, backend):
    backend = request.backend
    user = request.user
    user = backend.do_auth(
        access_token=request.data.get('access_token'),
        user=user.is_authenticated() and user or None
        )
    if user and user.is_active:
        print("el usuario vuelve")
        return user  # Return anything that makes sense here
    else:
        return None


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def social_register(request):
    auth_token = request.data.get('access_token', None)
    backend = request.data.get('backend', None)
    if auth_token and backend:
        try:
            user = auth_by_token(request, backend)
        except Exception, err:
            return Response(str(err), status=400)
        if user:
            strategy = load_strategy(request)
            uri = ''
            backend = load_backend(strategy, backend, uri)
            _do_login(backend, user, strategy)
            print("apunto de salir")
            pdb.set_trace()
            data = {
                    'name': user.username,
                    'id': user.id,
                    'status': user.status
                    }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Bad Credentials", status=403)
    else:
        return Response("Bad request", status=400)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer


class JugadoresViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    lookup_field = 'id'
    filter_backend = DjangoFilterBackend
    filter_fields = ('eventos', 'usuario', 'equipo')
    queryset = Jugador.objects.all()
    serializer_class = JugadoresSerializer


class EventosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer


class EquiposViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Equipos.objects.all()
    lookup_field = 'id'
    filter_backend = DjangoFilterBackend
    filter_fields = ('nombreDelGrupos', 'local_visitante')
    serializer_class = EquiposSerializer


class GruposViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Grupos.objects.all()
    serializer_class = GruposSerializer


class InvitacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Invitacion.objects.all()
    serializer_class = InvitacionSerializer