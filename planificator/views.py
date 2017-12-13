from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms.models import model_to_dict



def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login/')
    else:
        return redirect('login/')


def reglog_view(request):
    logout(request)
    form = SignUpForm()
    if request.method == 'POST':
        if 'register-submit' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/')
        elif 'login-submit' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile/')
            else:
                messages.error(request, 'Fallo al entrar.')
    return render(request, 'registration/login.html', {'form': form})

def profile_view(request):
    form = SignUpForm(instance=request.user)
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Sus datos han sido actualizados.')
            return redirect('/')
        else:
            messages.error(request, 'Fallo al modificar.')
            return redirect('/profile')
    return render(request, 'principal/profile.html', {'form': form})

def index(request):
     return render(request, 'main/index.html')

 # Create your views here.
def team_view(request):
    return render(request, 'main/index.html')
