from django import forms
from .models import Client

class NewClientForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name'}))
    charge = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Charge'}))

    class Meta:
        model = Client
        fields = ('name', 'charge',)
