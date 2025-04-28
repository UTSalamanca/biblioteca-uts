from django import forms
from .models import model_catalogo

class catalogo_form(forms.ModelForm):

    format = [
            ('Externo','Externo'),
            ('Interno','Interno')
            ]

    nom_libro = forms.CharField(label='Nombre del libro', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Nombre del libro', 'readonly':True}))
    nom_autor = forms.CharField(label='Nombre del autor', required=False, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Nombre del autor', 'readonly':True}))
    edicion = forms.CharField(label='Edición', required=False, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Edición', 'readonly':True}))
    colocacion = forms.CharField(label='Colocación', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Colocación', 'readonly':True}))
    formatoejem = forms.CharField(label='Formato', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Formato', 'readonly':True}))
    cantidad_i = forms.IntegerField(label='Cantidad inicial', required=True, widget=forms.NumberInput (attrs={'class':'form-control','placeholder':'Cantidad de ejemplares'}))
    tipoP = forms.ChoiceField(label='Tipo de Prestamo', choices=format, required=True, widget=forms.Select (attrs={'class':'form-select', 'placeholder':'Seleccione tipo de prestamo'}))

    class Meta:
        model = model_catalogo
        fields = ('nom_libro', 'nom_autor', 'edicion' ,'colocacion', 'formatoejem', 'cantidad_i', 'matricula', 'nom_alumno', 'carrera_grupo', 'tipoP')