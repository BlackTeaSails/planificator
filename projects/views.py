from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages
from django import forms

from clients.models import Client
from .models import Project, Requirement, GeneralRequirement, Assessment
from .forms import NewProjectForm

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
                project.stakeholders.add(stakeholder)
            project.save()
            messages.success(request, 'Proyecto: '+ project.name +' was added.')
            return redirect("/projects/page-1/")
    return render(request, 'projects/new_project.html', {'form': form,})

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/project_details.html', {'project':project})

# el metodo chungo que tiene que coger los requisitos abstractos y crear las copias asociadas
# eliminar los requisitos asociados a eliminar y etc. (dos multiselect)
def edit_project(request, project_id):
    return render(request, 'projects/projects_list.html', {})

# los requisitos asociados son mutables para adoptarse a las necesidades del cliente en cada momento en ese proyecto
def edit_requirement(request, requirement_id):
    return render(request, 'projects/projects_list.html', {})

# crea dos requisitos, el general y el
def new_requirement(request, project_id):
    return render(request, 'projects/projects_list.html', {})

def remove_project(request, project_id):
    project = Project.objects.all().get(id=project_id)
    # FALTA BORRAR y METER ENLACES PARA BORRAR EN LA PLANTILLA DE LISTAR proyectos
    messages.error(request, 'Proyecto: '+ project.name +' was deleted.', extra_tags='warning')
    return redirect("/projects/page-1/")

def projects_list(request, page_number):
    prefix = '/projects/page-'
    projects = Project.objects.filter(owner = request.user.id).order_by('creation_date')
    paginator = Paginator(projects, 10)
    last_page = int(paginator.num_pages)
    projects = paginator.page(page_number)
    # si page_number > last_page toma o last_page == 0, toma 404
    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'projects/projects_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'projects':projects})

# abstracción para que los usuarios regulares ni sepan que existe - vista para el admin.
def users_projects(request, user_id, page_number):
    # filtrar los proyectos por el usuario que nos pasen, luego hacer lo mismo que en el listar normal

    # añadir un if que comprueba si el usuario con el que trabajamos es el mismo que esta logueado,
    # si no lo es, añadir el nombre del usuario en la plantilla
    return render(request, 'projects/projects_list.html', {})
