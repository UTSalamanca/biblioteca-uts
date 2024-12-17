from django import forms
from .models import model_estadias
from static.helpers import dd

class estadias_form(forms.ModelForm):

    carrera_choice = [
        ("ADC","ADC"),
        ("MET", "MET"),
        ("QAI", "QAI"),
        ("PIA", "PIA"),
        ("QAM", "QAM"),
        ("ERC","ERC"),
        ("IDGS","IDGS"),
        ("ITEA","ITEA"),
        ("IMET","IMET"),
        ("IER","IER"),
        ("ISIP","ISIP"),
        ("IPQ","IPQ"),
        ("LGCH","LGCH")
        ]

    proyecto = forms.CharField(label='Proyecto', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control focusNext','placeholder':'Ingrese el nombre del proyecto', 'tabindex':'1'}))
    matricula = forms.IntegerField(label='Matricula', required=True, widget=forms.NumberInput (attrs={'class':'form-control focusNext','placeholder':'Ingrese la matricula del alumno', 'tabindex':'2'}))
    alumno = forms.CharField(label='Alumno', required=False, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Ingrese el nombre del alumno', 'readonly':True}))
    asesor_academico = forms.CharField(label='Asesor académico', required=False, max_length=255, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Nombre del asesor académico', 'readonly':True}))
    generacion = forms.CharField(label='Generación', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control focusNext','placeholder':'Indique la generación', 'tabindex':'3'}))
    empresa = forms.CharField(label='Empresa', required=True, max_length=255, widget=forms.TextInput (attrs={'class':'form-control focusNext','placeholder':'Ingrese el nombre de la empresa', 'tabindex':'4'}))
    asesor_orga = forms.CharField(label='Asesor Institucional', required=False, max_length=255, widget=forms.TextInput (attrs={'class':'form-control focusNext','placeholder':'Ingrese el asesor organizacional', 'tabindex':'5'}))
    carrera = forms.CharField(label='Carrera', required=True, widget=forms.TextInput (attrs={'class':'form-control','placeholder':'Indique la carrera', 'readonly':True}))
    reporte_file = forms.FileField(label='Reporte', required=True, widget=forms.FileInput(attrs={'class':'form-control', 'accept':'.pdf', 'placeholder':'Ingrese reporte en formato PDF' , 'tabindex':'6'}))

    class Meta:
        model = model_estadias
        fields = ('proyecto', 'matricula','alumno' ,'asesor_academico' ,'generacion','empresa','asesor_orga','carrera', 'reporte_file')