from django.db import models
from shopping_cart.models import Product
from accesos.models import Perfil
# Create your models here.

class Tour_Package(models.Model):
	title = models.CharField(max_length = 100,verbose_name = 'Titulo del Paquete')
	description = models.CharField(max_length = 250,verbose_name = 'Descripcion del Paquete')
	available_stock = models.IntegerField(default = 30 , verbose_name = 'Stock')
	company = models.CharField(max_length = 120, verbose_name = 'Compania')
	days = models.CharField(max_length = 150, verbose_name = 'Dia')
	hours = models.CharField(max_length = 100, verbose_name = 'Hora')
	price = models.IntegerField(default = 0, verbose_name = 'Precio')
	path_image = models.FileField(max_length= 250, verbose_name = 'Url de Imagen',blank=True, null = True)

	def __str__(self):
		return '{0} - {1}'.format(self.company,self.title)

class TourOrder(Product):

	tour = models.ForeignKey(Tour_Package, on_delete = models.SET_NULL, null = True)
	reservation_name = models.ForeignKey(Perfil,on_delete = models.SET_NULL, null = True)

	def __str__(self):
		return '{0} - {1}'.format(self.tour,self.reservation_name)
	