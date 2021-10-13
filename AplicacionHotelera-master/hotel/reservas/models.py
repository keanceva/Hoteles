from django.db import models
from accesos.models import Perfil
from django.db.models import Manager


# Create your models here.

class RoomType(models.Model):
	nombre = models.CharField(max_length = 150)	
	descripcion = models.CharField(max_length = 200)
	eliminado = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s. %s' % (self.id, self.nombre)

class Room(models.Model):	
	id_roomtype = models.ForeignKey(RoomType, on_delete = models.CASCADE , verbose_name ="Tipo de Habitación")
	#codigo = models.CharField(max_length=200,verbose_name="Código de Habitación")
	nombre = models.CharField(max_length=200,verbose_name="Nombre de Habitación")
	numero = models.IntegerField(verbose_name="Codigo de Habitación")
	descripcion = models.TextField(max_length = 300, verbose_name ="Descripcion de la Habitación")	
	# path_image = models.CharField(max_length = 500, verbose_name="Url de la imagen")
	path_image = models.FileField(upload_to='documents/',verbose_name = "Subir Imagen",max_length = 250)
	calificacion = models.IntegerField(default=0, verbose_name="Calificacion")
	num_camas = models.IntegerField(default=0, verbose_name="Numero de Camas")
	num_adultos = models.IntegerField(default=0, verbose_name="Numero de Adultos")
	num_ninos = models.IntegerField(default=0, verbose_name="Numero de Niños")
	precio = models.FloatField(default=0, verbose_name="Precio")
	disponible = models.BooleanField(default=True)		#True si esta disponible - False si esta reservada
	eliminado = models.BooleanField(default=False)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)


class BookingType(models.Model):
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 150)
	is_removed = models.BooleanField(default = False)
	create_date = models.DateTimeField(auto_now_add = True)
	update_date = models.DateTimeField(auto_now = True)

class BookingState(models.Model):
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 150)
	is_removed = models.BooleanField(default = False)
	create_date = models.DateTimeField(auto_now_add = True,  blank = True)
	update_date = models.DateTimeField(auto_now = True, blank = True)


#Reservas


class Booking(models.Model):
	
	customer_id = models.ForeignKey(Perfil, on_delete = models.CASCADE)
	room_id = models.ForeignKey(Room,on_delete = models.CASCADE)	
	state_id = models.ForeignKey(BookingState, on_delete = models.CASCADE)	
	check_in_date = models.DateTimeField(null= True) #Estas son las fechas de ingreso y salida en la reserva
	check_out_date = models.DateTimeField(null= True)
	fecha_ingresado = models.DateTimeField(null= True) #Estas son las fechas reales en las que el cliente ingresa al hotel
	fecha_salida = models.DateTimeField(null= True)
	num_adultos = models.IntegerField(default=0)
	num_ninos = models.IntegerField(default=0)
	no_nights = models.IntegerField(default = 0)
	total_to_pay = models.FloatField(default=0)
	is_removed = models.BooleanField(default = False)
	create_date = models.DateTimeField(auto_now_add = True)
	update_date = models.DateTimeField(auto_now = True)
	""" objects = Manager() """

	""" def get_total_price(self):

		room = Room.objects.filter(id=self.room_id).first()
		#Se debe implementar para que tambien sume el precio de los servicios despues agregados
		
		return room.precio """

#Checkout

class Checkout(models.Model):
	booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
	reason = models.CharField(max_length = 100)
	details_reason = models.TextField()
	amount = models.FloatField(default=0)
	is_canceled = models.BooleanField(default=False)
	details_canceled = models.TextField()
	is_removed = models.BooleanField(default=False)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)

#Prueba documento
class Document(models.Model):
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)