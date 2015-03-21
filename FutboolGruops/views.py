from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.views.generic import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Membership, Equipos, Grupos, User

# Create your views here.


@login_required(login_url='/login')
def home(request):
    if request.user.status:
        #traigo al objeto usuario
        usuario = User.objects.get(id=request.user.id)
        #traigo con el usuario los grupo
        gru = Membership.objects.filter(jugador=usuario)
        #traigo con un grupo todo los jugadores de ese grupo
        todos_los_usuarios = Membership.objects.filter(grupo=gru[0])
        #traigo con el grupo todo los equipos
        Todos_los_equipos = Equipos.objects.filter(nombreDelGrupos=gru[0])
        #traigo todo los jugadores por equipos
        jugador_v = User.objects.filter(equipos=Todos_los_equipos[0])
        jugador_l = User.objects.filter(equipos=Todos_los_equipos[1])
        #jugadores = zip(jugador_l,jugador_v)
        jugadores = list(zip(jugador_l, jugador_v))
        ctx = {'todos_los_usuarios': todos_los_usuarios,
            'nombreDelGrupo': gru[0].grupo.nombreDelGrupo,
            'Todos_los_equipos': Todos_los_equipos,
            'jugadores': jugadores,
            'equipo1': Todos_los_equipos[0],
            'equipo2': Todos_los_equipos[1],
            }
        return render(request, 'home.html', ctx)
    else:
        return redirect('registrar')


def error(request):
    return render_to_response('error.html',
                                context_instance=RequestContext(request))


@login_required(login_url='/login')
def invitacion(request):
    return render_to_response('invitacion.html',
                               context_instance=RequestContext(request))


@login_required(login_url='/login')
def invitar(request):
    #aca va la logica de la invitacion!
    #usuario = User.objects.get(user=request.user.id)
    #traigo con el usuario los grupo
    #gru = Membership.objects.filter(jugador=usuario)
    return render_to_response('invitar.html',
                                context_instance=RequestContext(request))


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
                     nombreDelGrupo=form_grupos.cleaned_data["nombreDelGrupo"])
                        #creo equipo local y visitante
                        equipo = Equipos.objects.create(
                            nombreDelEquipo=nombre_Equipo,
                            nombreDelGrupos=grupos,
                            local_visitante=True,
                            )
                        equipo_v = Equipos.objects.create(
                            nombreDelEquipo=nombre_Equipo_v,
                            nombreDelGrupos=grupos,
                            )
                        #guardamos equipo y usuario
                        equipo.save()
                        equipo_v.save()
                        request.user.equipos = equipo
                        request.user.save()
                        #guardamos los grupos
                        grupos.save()
                        #creo--
                        members = Membership(
                          jugador=User.objects.get(id=request.user.id),
                          grupo=grupos,
                          lugar=form_membership.cleaned_data.get('lugar'),
                          cancha_5=form_membership.cleaned_data.get('cancha_5'),
                          cancha_7=form_membership.cleaned_data.get('cancha_7'),
                        cancha_11=form_membership.cleaned_data.get('cancha_11'),
                          )
                        members.save()
                        return redirect('home')
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
