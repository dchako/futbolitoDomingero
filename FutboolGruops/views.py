from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext 
from django.views.generic import View
from .forms import ExtraDataForm, ExtraDataForm_grupos, ExtraDataForm_Membership, ExtraDataForm_Equipos
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login')
def home(request):
		if request.user.status:
			return render_to_response('home.html',context_instance=RequestContext(request))
		else:	
			return redirect ('/registrar')

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
		form_grupos = ExtraDataForm_grupos(instance=request.user.grupos)
		form_membership = ExtraDataForm_Membership(instance =request.user.membership)
		form_equipos = ExtraDataForm_Equipos(request.POST, instance =request.user.equipos)
		ctx = {'form_grupos':form_grupos,'form_equipos':form_equipos,'form_grupos':form_grupos,
				'form_membership':form_membership
				}
		return render (request, self.template_name, ctx)


	def post(self, request, *args, **kwargs):
		form = ExtraDataForm(request.POST)
		#form_grupos = ExtraDataForm_grupos(instance=request.user.grupos)
		#form_membership = ExtraDataForm_Membership(instance =request.user.membership)
		#form_equipos = ExtraDataForm_Equipos(request.POST, instance =request.user.equipos))
		if form.is_valid():
							# and form_equipos.is_valid() and form_grupos.is_valid():
			
			#aca va la logica de creacion de grupo
			request.user.username = request.POST['username']
			#form_grupos.save()
			#form_membership.save()
			#form_equipos.save()
			#request.user.email = request.POST['email']
			#request.user.first_name = request.POST['first_name']
			#request.user.last_name = request.POST['last_name']
			request.user.status = True
			request.user.save()
			return render(request,'home.html')
		else:
			error_username = form['username'].errors.as_text()
			#error_email = form['email'].errors.as_text()
			#error_first_name = form['first_name'].errors.as_text()
			#error_last_name = form['last_name'].errors.as_text()
			ctx = {'error_username':error_username, 
					#'error_email':error_email,
					#'error_first_name':error_first_name, 'error_last_name':error_last_name
					}
			return render (request, self.template_name, ctx)
