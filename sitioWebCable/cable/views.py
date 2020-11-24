from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Usuario
from .forms import UsuarioLogin,SeleccionForm,Proyecto,Catalogo, Seleccion


class loginView(View):
	model=Usuario
	succes_url = reverse_lazy('cable:all')
	template = 'cable/login.html'
	form = UsuarioLogin()

	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect('/')
		else:
			return render(request,self.template,{'form': self.form})

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			valuenext= request.POST.get('next')
			if(valuenext is not None):
				return HttpResponseRedirect(request.POST.get('next'))
			else:
				return HttpResponseRedirect('/login/')
		else:
			return redirect('/login/')
class logoutView(View):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect('/login/')

class mainView(LoginRequiredMixin,View):
	login_url = '/login/'
	succes_url = reverse_lazy('cable:all')
	template = 'cable/main.html'
	form = SeleccionForm()
	def get(self,request):
		return render(request, self.template, {'form': self.form})

	def post(self, request):
		form=SeleccionForm(request.POST)
		if form.is_valid():
			busquedaProyecto=Proyecto.objects.filter(idUsuario=request.user.pk)
			print(len(busquedaProyecto))
			if (len(busquedaProyecto)>0):
				corr = form.cleaned_data['corriente']
				ten = form.cleaned_data['tension']
				ins = form.cleaned_data['instalacion']
				mat = form.cleaned_data['material']
				nomProy = form.cleaned_data['nombreProyecto']
				proy = Proyecto.objects.get(idUsuario=request.user.pk)
				seleccion= Seleccion.objects.create(idUsuario=request.user,corriente=corr, tension=ten, instalacion=ins, material=mat, nombreProyecto=proy)
				seleccion.save()
				amp= seleccion.ampacidad()
				print("Busqueda    amp: "+str(amp)+", Material: "+str(mat))
				busquedaCatalogo=Catalogo.objects.filter(ampacidad=amp,material=mat)
				ctx = {'busquedaCatalogo': busquedaCatalogo}
				return render(request,'cable/result.html',ctx)
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponse("Formulario no valido")


def createUser(request):
	userName = ['juan.cobo','Esmeralda.gutierrez','Jake.grajales']
	nombre = ['Juan Cobos','Esmeralda Gutierrez','Jake Grajales']
	mail = ['juncobos@gmail.com','Esmeraldita45@gmail.com','jgrajales@gmail.com']
	estado = [True,True,True]
	pwd = ['Jun@s','Es*45','Jak180']
	#user1 = Usuario.objects.create_user(nombre='Juan Cobos',username='juan.cobo',correo='juncobos@gmail.com',password='Jun@s',estado=True)
	#user1.save()
	#user2 = Usuario.objects.create_user(nombre='Esmeralda.gutierrez',username='Esmeralda.gutierrez',correo='Esmeraldita45@gmail.com',password='Es*45',estado=True)
	#user2.save()
	#user3 = Usuario.objects.create_user(nombre='Jake.grajales',username='Jake Grajales',correo='jgrajales@gmail.com',password='Jak180',estado=True)
	#user3.save()
	#user4 = Usuario.objects.create_user(nombre='Jonatan Gonzalez',username='Jonatan.Gonzalez',correo='jgonzalez@gmail.com',password='casa123',estado=True)
	#user4.save()
	us=['juan.cobo','Jake.grajales']
	nomProy=['Cuestesitas1','Cuestesitas2']
	tipProy=['Conceptual','Ingeniería detalle']
	#proy = Proyecto(nombre='Cuestesitas1',tipoProyecto='Conceptual',idUsuario=user1)
	#proy.save()
	#proy2 = Proyecto(nombre='Cuestesitas2', tipoProyecto='Ingenieria detalle', idUsuario=user3)
	#proy2.save()
	proy3 = Proyecto(nombre='Cuestesitas3',tipoProyecto='Ingeniero de mantenimiento',idUsuario=user4)
	proy3.save()
	#for x in range(2):
		#uss=Usuario.objects.get(id=us[x])
		#proy = proy.objects.create(nombre=nomProy[x],tipoProyecto=tipProy[x],idUsuario=uss)
		#proy.save()
	return HttpResponse("Se creo")

def createCatalogo(request):
	cat1 = [1.26,	'cob',		13,		1,	3,	1,	25]
	cat2 = [2.5, 	'cob', 		110, 	2, 	5, 	2, 	50]
	cat3 = [1.26, 	'alu', 		20, 	1, 	3, 	3, 	25]
	cat4 = [2.5, 	'alu', 		130, 	2, 	5, 	4, 	50]
	cats=[cat1,cat2,cat3,cat4]
	for x in range(len(cats)):
		cat = cats[x]
		catalogo = Catalogo(codigoCable =cat[5],material =cat[1],espesorPantalla =cat[3] ,diametroCable =cat[4],ampacidad =cat[0],corriente =cat[6],tension =cat[2])
		catalogo.save()
	return HttpResponse("Se creo")

