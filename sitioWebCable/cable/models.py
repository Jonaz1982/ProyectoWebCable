from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
	username = models.CharField(max_length=30, unique=True)
	nombre= models.CharField(max_length=30)
	correo= models.CharField(max_length=50)
	password = models.CharField(max_length=128)
	estado= models.BooleanField()
	def getId(self):
		return self.id
	def verificarIngreso(self,pwd,user):
		if (pwd==self.contrasena and user==self.id):
			return True
		else:
			return False
class Proyecto(models.Model):
	nombre= models.CharField(primary_key=True,max_length=30)
	tipoProyecto = models.CharField(max_length=30)
	idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	def verificarPermiso(self):
		print()

class Catalogo(models.Model):
	cobre='cob'
	aluminio='alu'
	materiales=(
		(cobre,'cobre'),
		(aluminio,'aluminio')
	)
	codigoCable = models.AutoField(primary_key=True)
	material = models.CharField(max_length=3,choices=materiales,default=cobre)
	espesorPantalla = models.IntegerField()
	diametroCable = models.IntegerField()
	ampacidad =  models.FloatField()
	corriente = models.IntegerField()
	tension = models.IntegerField()
	def buscarSemejante(self,amp,mat):
		if(amp==self.ampacidad,mat==self.material):
			return self.codigoCable
class Cable(models.Model):
	idUsuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
	ampacidadS=0.0
	fechaIntento = models.DateTimeField(auto_now_add=True)
	def correrSeleccion(self, amp, verificarPermiso):
		if(verificarPermiso):
			self.ampacidadS=amp


class Seleccion(models.Model):
	cobre='cob'
	aluminio='alu'
	materiales=(
		(cobre,'cobre'),
		(aluminio,'aluminio')
	)
	idUsuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
	fechaBusqueda = models.DateTimeField(auto_now_add=True)
	corriente= models.IntegerField()
	tension=models.IntegerField()
	instalacion = models.CharField(max_length=50)
	material = models.CharField(max_length=3,choices=materiales,default=cobre)
	nombreProyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	def ampacidad(self):
		amp=0.0
		if (self.corriente<40):
			return 1.26
		else:
			return 2.5
		return amp