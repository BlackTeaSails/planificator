from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Contraseña nueva'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirmación de la contraseña'}))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2', )

class SignUpForm(UserCreationForm):

    attributos = {'class': 'form-control'}
    email = forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de usuario'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirmación de la contraseña'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class OwnProfileForm(UserChangeForm):
    email = forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de usuario'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class ModifyForm(forms.ModelForm):

    email = forms.CharField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de usuario'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
