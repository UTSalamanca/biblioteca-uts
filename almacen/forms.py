from django import forms
from .models import acervo_model

class registro_form(forms.ModelForm):
    
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    titulo = forms.CharField(label='Titulo', required=True, max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese el titulo'}))
    autor = forms.CharField(label='Autor', max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese el autor'}))
    editorial = forms.CharField(label='Editorial', max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese la editorial'}))
    cant = forms.IntegerField(label='Cantidad', required=True, widget=forms.NumberInput (attrs={'class':'form-control','placeholder':'Indique la cantidad de libros'}))
    colocacion = forms.CharField(label='Colocación', required=True, max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese la colocacion'}))
    edicion = forms.CharField(label='Edición', max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese la edición'}))
    anio = forms.IntegerField(label='Año', widget=forms.NumberInput (attrs={'class':'form-control','placeholder':'Ingrese el año de edición'}))
    adqui = forms.CharField(label='Tipo de adquisición', max_length=100, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'indique el tipo de adquisición'}))
    formato = forms.ChoiceField(label='Formato', choices=acervo_model.Format.choices, required=True, widget=forms.Select (attrs={'class':'form-select','placeholder':'Indique el formato del libro'}))
    estado = forms.ChoiceField(label='Estado', choices=acervo_model.State.choices, required=True, widget=forms.Select (attrs={'class':'form-select','placeholder':'Indique el estado del libro'}))
    class Meta:
        model = acervo_model
        fields = ('id', 'titulo','autor','editorial','cant','colocacion','edicion','anio','adqui','formato','estado')