from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, ModifyForm, OwnProfileForm, CustomSetPasswordForm # Para crear y modificar usuarios
from django.shortcuts import render, redirect
from django.contrib import messages # error and success messages
from django.forms.models import model_to_dict # i doent remember what that was for
from django.contrib.auth.models import User # password recovery
from django.core.exceptions import ObjectDoesNotExist # password recovery - getting user by email
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page


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
            else:
                return render(request, 'registration/login.html', {'form': form, 'registro': "True"})
        elif 'login-submit' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/auth/profile/')
            else:
                messages.error(request, 'Fallo al entrar.', extra_tags='warning')
    return render(request, 'registration/login.html', {'form': form, 'registro': "False"})

def profile_view(request):
    prefix = '/auth/profile/'
    form = ModifyForm(instance=request.user)
    if request.method == 'POST':
        form = ModifyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sus datos han sido actualizados.')
        else:
            messages.error(request, 'Fallo al modificar.', extra_tags='danger')
    return render(request, 'principal/profile.html', {'form': form, 'prefix':prefix, 'user_profile':request.user})

def change_pass(request):
    prefix = '/auth/change_pass/'
    form_pass = CustomSetPasswordForm(request.user)
    if request.method == 'POST':
        form_pass = CustomSetPasswordForm(request.user, request.POST)
        if form_pass.is_valid():
            form_pass.save()
            username = request.user.username
            raw_password = form_pass.cleaned_data.get('new_password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Su contraseña ha sido actualizadas.')
        else:
            messages.error(request, 'Fallo al modificar la contraseña.', extra_tags='danger')
    return render(request, 'principal/profile.html', {'form': form_pass, 'prefix':prefix, 'user_profile':request.user})

def modify_user(request, user_id):
    prefix = '/auth/edit/user-' + user_id + '/'
    form = ModifyForm(instance=User.objects.get(id=user_id))
    if request.method == 'POST':
        form = ModifyForm(request.POST, instance=User.objects.get(id=user_id))
        if form.is_valid():
            is_author = False
            if request.POST.get('is_author', False):
                is_author = True
            is_internal = False
            if request.POST.get('is_personal', False):
                is_internal = True
            # print("es un autor:", is_author, "y ademas personal interno: ", is_internal)

            form.save()
            messages.success(request, 'Los datos del usuario han sido actualizados.')
        else:
            messages.error(request, 'Fallo al modificar.', extra_tags='danger')
    return render(request, 'principal/profile.html', {'form': form, 'prefix':prefix, 'user_profile':User.objects.get(id=user_id)})


def user_list(request, page_number):
    users = User.objects.order_by('id')
    paginator = Paginator(users, 15)
    last_page = int(paginator.num_pages)
    users = paginator.page(page_number)
    # si page_number > last_page toma o last_page == 0, toma 404
    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'registration/users.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'users':users})


def recover_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User()
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = None

        if user is not None:
            # aqui se genera una contraseña nueva y se envia esta por email a través del gestor de mensajeria correspondiente.
            messages.success(request, 'Se ha generado una contraseña nueva que ha sido enviada a su email.')
        else:
            messages.error(request, 'No se lo quien me dices.', extra_tags='warning')
    return render(request, 'registration/recover.html', {})


def remove_user(request, user_id):
    try:
        u = User.objects.get(id=user_id)
        u.delete()
        messages.sucess(request, "The user was deleted")
    except:
        messages.error(request, "The user was not found", extra_tags='danger')
    return redirect('/auth/users/page-1/')
