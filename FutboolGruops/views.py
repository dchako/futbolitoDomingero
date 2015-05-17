from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.views.generic import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Eventos, Equipos, Grupos, User, Jugador, Invitacion
from django.http import HttpResponse
import json
from django.http import Http404
# Create your views here.


@login_required(login_url='/login')
def home(request, id):
    if request.user.status:
        #traigo con el usuario todos los  evento del usuario!
        eventoDadmins = Jugador.objects.filter(usuario=request.user.id)
        #esta es la linea diferente de home
        #cosas raras
        if id == '0':
            print(id)
            print("aca entro")
            todos_los_usuarios = Jugador.objects.filter(
                                                  eventos=eventoDadmins[0])
            eventoDadmin = Eventos.objects.get(id=eventoDadmins[0].id)
        else:
            print (id)
            print("distinto de cero")
            eventoDadmin = Eventos.objects.get(id=id)
            #traigo con un evento todo los jugadores de ese evento
            todos_los_usuarios = Jugador.objects.filter(eventos=eventoDadmin)

        cantidad = todos_los_usuarios.count
        asis = Jugador.objects.filter(eventos=eventoDadmin, asistencia=True)
        asisten = asis.count
        Todos_los_equipos = Equipos.objects.filter(
                    nombreDelGrupos=eventoDadmin)
        jugador_v = Jugador.objects.filter(
                        eventos=eventoDadmin.id,
                        equipo=Todos_los_equipos[0])
        jugador_l = Jugador.objects.filter(
                        eventos=eventoDadmin.id,
                        equipo=Todos_los_equipos[1])
        jugadores = list(zip(jugador_l, jugador_v))
        obj_invit = Invitacion.objects.filter(
        usuario_invitado=request.user.id,
        estado=False,)
        cant = obj_invit.count

        ctx = {'todos_los_usuarios': todos_los_usuarios,
            'nombreDelGrupos': eventoDadmins,
            'nombreDelGrupo': eventoDadmin.nombreDGrupos.nombreDelGrupo,
            'Todos_los_equipos': Todos_los_equipos,
            'jugadores': jugadores,
            'equipo1': Todos_los_equipos[0],
            'equipo2': Todos_los_equipos[1],
            'asisten': asisten,
            'cantidad': cantidad,
            'cant': cant,
            'ids': id,
            }
        return render(request, 'home.html', ctx)
    else:
        return redirect('registrar')


def error(request):
    return render_to_response('error.html',
                                context_instance=RequestContext(request))


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
            print(grupe)
            obj_evento = Eventos.objects.get(
                            usuarioCreador=obj_usuario, nombreDGrupos=grupe)
            g = Jugador.objects.get(
                        usuario=obj_usuario, eventos=obj_evento.id)
            if(accionista == '1'):
                g.asistencia = True
            else:
                g.asistencia = False
            g.save()
            data['code'] = 'OK'
        except User.DoesNotExist:
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
        print(ids)
        data = {}
        try:
            obj_invit = Invitacion.objects.get(id=ids)
            print("acasdas")
            equipos = Equipos.objects.filter(nombreDelGrupos=obj_invit)
            if(accionista == '1'):
                print("aca entro")
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
        except User.DoesNotExist:
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
                    nombreDelGrupo=grupete, usuarioCreador=obj_usuario)
            obj_evento = Eventos.objects.get(
                            usuarioCreador=obj_usuario, nombreDGrupos=grupe)
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
        except User.DoesNotExist:
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
        except User.DoesNotExist:
            data['code'] = 'ERROR'
            data['message'] = 'No se encontro ningun registro'
        return HttpResponse(
                json.dumps(data), content_type='application/json')
    else:
        raise Http404


@login_required(login_url='/login')
def invitar(request, id):
    eventoDadmin = Eventos.objects.filter(
                                usuarioCreador=request.user.id)
    eventoDadmins = Eventos.objects.get(id=id)
    if request.POST:
        try:
            usuario = User.objects.get(username=request.POST["username"])
            grupoAdmin = Eventos.objects.filter(usuarioCreador=usuario)
            EventoAdmin = Jugador.objects.filter(eventos=grupoAdmin[0].id)
        except User.DoesNotExist:
            mensaje = "No Existe el usuario"
            ctx = {'form': ExtraDataForm(request.POST),
                    'nombreDelGruposs': eventoDadmin,
                 'nombreDelGrupo': eventoDadmins.nombreDGrupos.nombreDelGrupo,
                'error': mensaje, }
            return render(request, 'invitar.html', ctx,
                                    context_instance=RequestContext(request))
        mensaje = ""
        ctx = {'nombre_jugador': usuario,
            'nombreDelGrupos': grupoAdmin[0].nombreDGrupos,
            'nombreDelGrupo': eventoDadmins.nombreDGrupos.nombreDelGrupo,
            'equipo_local': EventoAdmin[0].equipo,
            'nombreDelGruposs': eventoDadmin,
            'error': mensaje,
            'form': ExtraDataForm(request.POST),
            }
        return render(request, 'invitar.html', ctx,
                                    context_instance=RequestContext(request))
    mensaje = ""
    ctx = {
        'form': ExtraDataForm(request.POST),
        'error': mensaje,
        'nombreDelGrupo': eventoDadmins.nombreDGrupos.nombreDelGrupo,
        'nombreDelGruposs': eventoDadmin,
        }
    return render_to_response('invitar.html', ctx,
                                    context_instance=RequestContext(request))


@login_required(login_url='/login')
def estrategias(request, id):
        #traigo con el usuario todos los  evento del usuario!
        eventoDadmins = Jugador.objects.filter(usuario=request.user.id)
        #esta es la linea diferente de home
        #cosas raras
        if id == '0':
            eventoDadmin = Eventos.objects.get(id=eventoDadmins[0].id)
        else:
            eventoDadmin = Eventos.objects.get(id=id)
            #traigo con un evento todo los jugadores de ese evento

        obj_invit = Invitacion.objects.filter(
                    usuario_invitado=request.user.id,
                    estado=False,)
        cant = obj_invit.count
        ctx = {
            'nombreDelGrupos': eventoDadmins,
            'nombreDelGrupo': eventoDadmin.nombreDGrupos.nombreDelGrupo,
            'cant': cant,
            'ids': id,
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
                        jug.save()
                        return redirect('home' '0')
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
                print("entro aca")
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