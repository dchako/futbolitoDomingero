from django import forms
from .models import User 


class ExtraDataForm(forms.ModelForm):


	class Meta:
		model = User
		fields = ('username', 'email', 'first_name' , 'last_name')