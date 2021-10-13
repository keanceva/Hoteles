from django.db import models
from django.db.models import Manager

# Create your models here.

class Noticia(models.Model):
    titulo = models.CharField(max_length = 150)
    noticia = models.TextField(verbose_name ="Noticia completa")
    path_image = models.FileField(upload_to='documents/',verbose_name = "Subir Imagen",max_length = 250)
    create_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True)
