from django import forms
from .models import Tercero, Material

class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'