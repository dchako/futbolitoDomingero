from django import forms
from .models import User #, Membership, Grupos, Equipos 


class ExtraDataForm(forms.ModelForm):


	class Meta:
		model = User
		fields = ('username', 
			#'email', 'first_name' , 'last_name'
			)

"""
class ExtraDataForm_grupos(forms.ModelForm):


	class Meta:
		model = Grupos
		fields = ('username', 'members')


class ExtraDataForm_Membership(forms.ModelForm):


	class Meta:
		model = Membership
		fields = ('jugador','grupo' ,'dias_horas','lugar', 'asistencia')


class ExtraDataForm_Equipos(forms.ModelForm):


	class Meta:
		model = Equipos
		fields = ('nombre','visitante_local')
"""