from django.forms import ModelForm
from django import forms
from cable.models import Usuario,Seleccion,Proyecto,Catalogo
from django.contrib.auth.forms import AuthenticationForm

class UsuarioLogin(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Usuario
		fields = ['username', 'password']
	def __init__(self, *args, **kwargs):
		super(UsuarioLogin, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['password'].label = "Contraseña"
class UsuarioAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass


class SeleccionForm(ModelForm):
	class Meta:
		model=Seleccion
		fields = ['corriente','tension','instalacion','material','nombreProyecto']