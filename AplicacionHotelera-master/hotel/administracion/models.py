from django.db import models

# Create your models here.

class Publicidad(models.Model):
	#imagen=models.ImageField(upload_to = 'static/imagenes', default='static/imagenes/no-img.jpg')
	imagen = models.FileField(upload_to='anuncios/',max_length= 250, verbose_name = 'Url de Imagen',blank=True, null = True)
	name = models.CharField(max_length=100, verbose_name = 'Nombre del Anuncio')
	date=models.DateTimeField(auto_now_add=True, blank=True)
	company=models.CharField(max_length=100, verbose_name = 'Compania')
	price=models.FloatField(verbose_name = 'Precio por Publicitar')
	hits = models.IntegerField(verbose_name = 'Hits del Anuncio', default = 0)
	phone=models.CharField(max_length=250,null=True,verbose_name = 'Telefono Contacto')
	city=models.CharField(max_length=250,null=True,verbose_name = 'Ciudad Contacto')
	address=models.CharField(max_length=250,null=True,verbose_name = 'Direccion Contacto')

