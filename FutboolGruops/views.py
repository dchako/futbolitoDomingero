from django.shortcuts import render_to_response, render ,redirect
from django.template import RequestContext 
from django.views.generic import View
from .forms import ExtraDataForm, ExtraDataForm_grupos, ExtraDataForm_Membership, ExtraDataForm_Equipos
from django.contrib.auth.decorators import login_required
from .models import Membership, Equipos, Grupos, User

# Create your views here.
@login_required(login_url = '/login')
def home(request):
		if request.user.status:
			usuario = User.objects.get(id = request.user.id)
			gru = Membership.objects.filter(jugador = usuario)
			usuarios = Membership.objects.filter(grupo = gru[0])

			ctx ={'usuarios':usuarios,
				  'nombreDelGrupo':gru[0].grupo.nombreDelGrupo,
				 }
			return render (request, 'home.html', ctx)
		else:
			return render (request, 'registrar.html')

def error(request):
	return render_to_response('error.html',context_instance=RequestContext(request))

@login_required(login_url = '/login')
def invitacion(request):
	return render_to_response('invitacion.html',context_instance=RequestContext(request))

@login_required(login_url = '/login')
def invitar(request):
	return render_to_response('invitar.html',context_instance=RequestContext(request))

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))


class ExtraDataView(View):

	template_name = 'registrar.html'
	

	def get(self , request, *args, **kwargs):
	
		ctx = {'form_grupos':ExtraDataForm_grupos(prefix="Grupos"),
				'form_equipos':ExtraDataForm_Equipos(instance =request.user.equipos),
				'form_membership':ExtraDataForm_Membership(prefix="Membership"),
				'form':ExtraDataForm(request.POST),
				}
		return render (request, self.template_name, ctx)


	def post(self, request, *args, **kwargs):
		
		form = ExtraDataForm(request.POST)
		form_grupos = ExtraDataForm_grupos(request.POST, prefix="Grupos")
		form_membership = ExtraDataForm_Membership(request.POST,prefix="Membership")
		form_equipos = ExtraDataForm_Equipos(request.POST,instance =request.user.equipos)
		form_equipos_vis = ExtraDataForm_Equipos(request.POST['nombreDelEquipo_v'])
		if form_equipos.is_valid() and form_grupos.is_valid() and form_membership.is_valid() and form_equipos_vis.is_valid():
			#aca guardamos usuario y equipos
			if form.is_valid(): 
				request.user.username = request.POST['username']
			else:
				request.user.username = request.user.username

			request.user.status = True 
			nombre_Equipo = form_equipos.cleaned_data["nombreDelEquipo"]
			nombre_Equipo_v = request.POST['nombreDelEquipo_v']
			print nombre_Equipo 
			print nombre_Equipo_v
			#grupo antes
			nombre_Grupo=form_grupos.cleaned_data["nombreDelGrupo"]
			grupos = Grupos.objects.create(nombreDelGrupo= nombre_Grupo)
			equipo = Equipos.objects.create(nombreDelEquipo = nombre_Equipo, nombreDelGrupos=grupos)
			equipo_v = Equipos.objects.create(nombreDelEquipo = nombre_Equipo_v, nombreDelGrupos=grupos)
			#guardamos equipo y usuario
			equipo.save()
			equipo_v.save()
			request.user.equipos = equipo
			request.user.save()
			#creamos la membresia
			usuario = User.objects.get(id = request.user.id)
			lugarejo = form_membership.cleaned_data.get('lugar')
			members = Membership(jugador=usuario, grupo=grupos, lugar = lugarejo)
			members.save()
			return redirect('home')
		else:
			ctx = { 
				'error_username':form['username'].errors.as_text(),
				'error_diaDeJuegoYhoras':form_membership['dias_horas'].errors.as_text(),
				'error_lugar':form_membership['lugar'].errors.as_text(),	
				'error_nombreDelGrupo':form_grupos['nombreDelGrupo'].errors.as_text(),	
				'error_nombreDeEquipoLocal':form_equipos['nombreDelEquipo'].errors.as_text(),
				'error_nombreDelEquipoVisitante':form_equipos['nombreDelEquipo'].errors.as_text(),
				'error_form_equipos_visitante':form_equipos_vis['nombreDelEquipo'].errors.as_text(),
				'form_grupos':form_grupos,
				'form_equipos':form_equipos,
				'form_grupos':form_grupos,
				'form_membership':form_membership,
				'form':form
				  }
			return render (request, self.template_name, ctx)
