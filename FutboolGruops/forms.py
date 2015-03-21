from django import forms
from .models import User, Membership, Grupos, Equipos


class ExtraDataForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',
                    #'email', 'first_name' , 'last_name'
                    )


class ExtraDataForm_grupos(forms.ModelForm):

    class Meta:
        model = Grupos
        fields = ('nombreDelGrupo',)


class ExtraDataForm_Membership(forms.ModelForm):

    class Meta:
        model = Membership
        fields = ('dias_horas', 'lugar', 'cancha_5', 'cancha_7', 'cancha_11')


class ExtraDataForm_Equipos(forms.ModelForm):

    class Meta:
        model = Equipos
        fields = ('nombreDelEquipo', )