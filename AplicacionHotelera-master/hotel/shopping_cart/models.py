from django.db import models

from reservas.models import Booking
from accesos.models import Perfil

# Create your models here.

#Clase padre para paquetes turisticos o servicios adicionales
class Product(models.Model):
	title = models.CharField(max_length = 100, verbose_name = 'Titulo')
	description = models.CharField(max_length = 250,verbose_name = 'Descripcion del Producto')
	quantity = models.IntegerField(default = 30,verbose_name = 'Cantidad')


class OrderItem(models.Model):
	product = models.OneToOneField(Product, on_delete = models.SET_NULL, null = True)
	is_ordered = models.BooleanField(default=False)
	price = models.FloatField(default = 0)
	date_added = models.DateTimeField(auto_now = True)
	date_ordered = models.DateTimeField(null=True)


class Order(models.Model):

	reference_code = models.CharField(max_length = 12)
	owner = models.ForeignKey(Perfil,on_delete= models.SET_NULL,null=True)
	is_ordered = models.BooleanField(default = True)
	items = models.ManyToManyField(OrderItem)

	def get_items(self):
		return self.items.all()

	def get_cart_total(self):
		return sum([item.reserva.get_total_price(item.product) for item in self.items.all()])

	def __str__(self):
		return '{0} - {1}'.format(self.owner,self.reference_code)
