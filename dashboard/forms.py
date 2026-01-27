from django import forms
from .models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subjects', 'title', 'description', 'due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=255, label="Search anything you want ")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']


class BaseConversionForm(forms.Form):
    value = forms.FloatField(required=False, label=False, widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Number'
        }
    ))
    
    measure1 = forms.ChoiceField(label='', widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    measure2 = forms.ChoiceField(label='', widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    CHOICES = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['measure1'].choices= self.CHOICES
        self.fields['measure2'].choices= self.CHOICES


class ConversionForm(forms.Form):
    CHOICES = [
        ('length', 'Length'),
        ('mass', 'Mass')
    ]
    measurement = forms.ChoiceField(choices= CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(BaseConversionForm):
    CHOICES = [
        ('yard', 'Yard'), 
        ('foot', 'Foot')
    ]

        
class ConversionMassForm(BaseConversionForm):
    CHOICES = [
        ('pound', 'Pound'), 
        ('kilogram', 'Kilogram')
    ]
    
    