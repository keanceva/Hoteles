from django import forms

from tour_package.models import Tour_Package,TourOrder

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

class TourOrderForm(forms.ModelForm):

	class Meta:
		model = TourOrder

		fields = '__all__'

		widgets = {

			'title': forms.HiddenInput(attrs={'class':'form-control'}),
			'tour': forms.HiddenInput(attrs={'class':'form-control'}),
			'description': forms.HiddenInput(attrs={'class':'form-control'}),
			'reservation_name': forms.HiddenInput(attrs={'class':'form-control'}),
			'quantity': forms.NumberInput(attrs={'class':'form-control'}),
		}
