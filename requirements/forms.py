from django import forms
from .models import Requirement

class NewRequirementForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'description'}))
    effort = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'effort'}))

    class Meta:
        model = Requirement
        fields = ('name', 'description', 'effort')
