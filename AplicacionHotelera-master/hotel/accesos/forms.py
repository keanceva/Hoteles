from django import forms
from accesos.models import Perfil

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Perfil

        fields = '__all__'

        widgets = {
            'usr_id': forms.HiddenInput(attrs={'class':'form-control'}),
            'is_removed': forms.HiddenInput(attrs={'class':'form-control'}),
            'create_date': forms.HiddenInput(attrs={'class':'form-control'}),
            'update_date': forms.HiddenInput(attrs={'class':'form-control'}),
        }