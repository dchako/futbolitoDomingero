from django.shortcuts import render_to_response
from django.template import RequestContext 

# Create your views here.
def home(request):
    return render_to_response('home.html',context_instance=RequestContext(request))

def error(request):
	return render_to_response('error.html',context_instance=RequestContext(request))

def invitacion(request):
	return render_to_response('invitacion.html',context_instance=RequestContext(request))

def invitar(request):
	return render_to_response('invitar.html',context_instance=RequestContext(request))

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def registrar(request):
	return render_to_response('registrar.html',context_instance=RequestContext(request))