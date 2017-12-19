from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages
from django import forms

from clients.models import Client
from .models import Project, Requirement, GeneralRequirement, Power, Assessment
from .forms import NewProjectForm, NewRequirementForm

def add_project(request):
    clients = Client.objects.filter(owner = request.user.id)
    form = NewProjectForm()
    form.fields['stakeholders'] = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), queryset=clients)
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            stakeholders = request.POST.getlist('stakeholders')
            project.save()
            for stakeholder in stakeholders:
                power = Power(project=project, client=Client.objects.all().get(id=stakeholder))
                power.save()
            project.save()
            messages.success(request, 'Project: '+ project.name +' was added.')
            return redirect("/projects/page-1/")
    return render(request, 'projects/new_project.html', {'form': form,})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        weight = request.POST.get('weight')
        client_id = request.POST.get('client_id')
        power = Power.objects.all().get(client=client_id, project=project.id)
        power.weight = weight
        power.save()
        messages.success(request, power.client.name +'\'s weight in this project was edited.')
    return render(request, 'projects/project_details.html', {'project':project})

def projects_list(request, page_number):
    prefix = '/projects/page-'
    projects = Project.objects.filter(owner = request.user.id).order_by('creation_date')
    paginator = Paginator(projects, 10)
    last_page = int(paginator.num_pages)
    projects = paginator.page(page_number)

    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'projects/projects_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'projects':projects})

def users_projects(request, user_id, page_number):
    prefix = '/projects/page-'
    projects = Project.objects.filter(owner = user_id).order_by('creation_date')
    paginator = Paginator(projects, 10)
    last_page = int(paginator.num_pages)
    projects = paginator.page(page_number)

    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'projects/projects_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'projects':projects})

# el metodo chungo que tiene que coger los requisitos abstractos y crear las copias asociadas
# eliminar los requisitos asociados a eliminar y etc. (dos multiselect)
def edit_project(request, project_id):
    return render(request, 'projects/projects_list.html', {})

def remove_project(request, project_id):
    project = Project.objects.all().get(id=project_id)
    project.delete()
    messages.error(request, 'Projects: '+ project.name +' was deleted.', extra_tags='warning')
    return redirect("/projects/page-1/")

# crea dos requisitos, el general y el asociado a ese proyectos
def new_requirement(request, project_id):
    form = NewRequirementForm()
    if request.method == 'POST':
        form = NewRequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save(commit=False)
            project = Project.objects.all().get(id=project_id)
            requirement.project = project
            requirement.save()
            # FALTA crear un GeneralRequirement para reutilizarlo
            for stakeholder in project.stakeholders.all():
                assesment = Assessment(client=stakeholder, requirement=requirement )
                assesment.save()
            requirement.save()
            messages.success(request, 'Requirement: '+ requirement.name +' was created.')
            return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')
    return render(request, 'requirements/new_requirement.html', {'form':form})

def edit_requirement(request, requirement_id):
    requirement = Requirement.objects.get(id=requirement_id)
    form = NewRequirementForm(instance=requirement)
    if request.method == 'POST':
        form = NewRequirementForm(request.POST, instance=requirement)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.save()
            messages.success(request, 'Requirement: '+ requirement.name +' was modified.')
            return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')
    return render(request, 'requirements/new_requirement.html', {'form':form})

def toggle_requirement(request, requirement_id):
    requirement = Requirement.objects.all().get(id=requirement_id)
    requirement.state = not requirement.state
    requirement.save()
    if requirement.state:
        messages.success(request, 'Requirement: '+ requirement.name +' marked as done.')
    else:
        messages.error(request, 'Requirement: '+ requirement.name +' unmarked as done.', extra_tags='warning')
    return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')

# falta borrar de la base de datos
def remove_requirement(request, requirement_id):
    requirement = Requirement.objects.all().get(id=requirement_id)
    # BORRAR DE LA BBDD
    messages.error(request, 'Requirement: '+ requirement.name +' was deleted from the project.', extra_tags='warning')
    return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')
