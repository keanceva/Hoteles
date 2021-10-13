from django import forms
from django.forms import Textarea
from .models import Publicidad
from reservas.models import Room, RoomType, Document
from tour_package.models import Tour_Package
from noticias.models import Noticia

class RoomForm(forms.ModelForm):

	class Meta:
		model = Room

		fields = "__all__"

		# field_test = forms.ModelChoiceField(queryset=RoomType.objects.all(), to_field_name="id", empty_label=None)

		widgets = {
			# 'codigo': forms.TextInput(attrs={'class':'form-control'}),			
			#'titulo': forms.TextInput(attrs={'class':'form-control'}),
			# 'id_roomtype': form.ModelChoiceField(queryset=RoomType.objects.all(), to_field_name="id"),
			'id_roomtype': forms.Select(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'numero': forms.NumberInput(attrs={'class':'form-control'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control'}),
			'calificacion': forms.HiddenInput(attrs={'class':'form-control'}),
			# 'path_image':forms.FileInput(attrs={'class':'form-control'}),
			#'path_image':forms.TextInput(attrs={'class':'form-control'}),
			'num_camas': forms.NumberInput(attrs={'class':'form-control'}),
			'num_adultos': forms.NumberInput(attrs={'class':'form-control'}),
			'num_ninos': forms.NumberInput(attrs={'class':'form-control'}),
			'precio':forms.NumberInput(attrs={'class':'form-control'}),
			'disponible': forms.HiddenInput(attrs={'class':'form-control'}),		
			'eliminado': forms.HiddenInput(attrs={'class':'form-control'}),
		}

class TourForm(forms.ModelForm):

	class Meta:
		model = Tour_Package

		fields = [
			'title',
			'description',
			'company',
			'days',
			'hours',
			'price',
			'available_stock',
			'path_image',
		]

		labels = {
			'title':'Titulo del Paquete',
			'description':'Descripcion del Paquete',
			'company':'Compañia',
			'days':'Dias del Tour',
			'hours':'Horas del Tour',
			'price':'Precio del Paquete',
			'available_stock': 'Cupos Disponibles',
			'path_image':'Subir Imagen',
		}

		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.TextInput(attrs={'class':'form-control'}),
			'company':forms.TextInput(attrs={'class':'form.control'}),
			'days':forms.TextInput(attrs={'class':'form-control'}),
			'hours':forms.TextInput(attrs={'class':'form-control'}),
			'price':forms.NumberInput(attrs={'class':'form-control'}),
			'available_stock':forms.NumberInput(attrs={'class':'form-control'}),
			'path_image':forms.FileInput(attrs={'class':'form-control'}),

		}

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('description', 'document', )

class NoticiaForm(forms.ModelForm):
	class Meta:
		model = Noticia

		fields = {
			'titulo',
			'noticia',
			'path_image',
		}

		labels = {
			'titulo' : 'Titulo de la noticia',
			'noticia' : 'Noticia completa',
			'path_image' : 'Subir imagen',
		}

		widgets = {
			'titulo' : forms.TextInput(attrs={'class':'form-control'}),
			'noticia' : Textarea(attrs={'class':'form-control'}),
			'path_image' : forms.FileInput(attrs={'class':'form-control'}),
		}

class PublicidadForm(forms.ModelForm):
   class Meta:
      model = Publicidad
      fields = ['imagen','name','company','price','phone','city','address']

      widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control'}),
			'company' : forms.TextInput(attrs={'class':'form-control'}),
			'price' : forms.NumberInput(attrs={'class':'form-control'}),
			'imagen' : forms.FileInput(attrs={'class':'form-control'}),
			'phone' : forms.TextInput(attrs={'class':'form-control'}),
			'city' : forms.TextInput(attrs={'class':'form-control'}),
			'address' : forms.TextInput(attrs={'class':'form-control'})
		}


