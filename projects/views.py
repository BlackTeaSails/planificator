from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages
from django import forms

from clients.models import Client
from requirements.models import Requirement
from .models import Project, Power
from .forms import NewProjectForm, EditProjectForm

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

def edit_project(request, project_id):
    project = Project.objects.all().get(id=project_id)
    form = EditProjectForm(instance=project)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project: '+ project.name +' was edited.')
            return redirect("/projects/page-1/")
    return render(request, 'projects/edit_project.html', {'form': form,'project': project,})

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

def remove_project(request, project_id):
    project = Project.objects.all().get(id=project_id)
    project.delete()
    messages.success(request, 'Projects: '+ project.name +' was deleted.')
    return redirect("/projects/page-1/")

def next_release(request, project_id):
    project = Project.objects.all().get(id=project_id)
    requirements = Requirement.objects.all().filter(project=project).filter(last_released=True)

    incomplete, zero_influencies, zero_assessments = project.checkFillables()
    if request.method != 'POST' and incomplete:
        messages.error(request, 'We have detected that there is lack of the following data, please, complete those before using this functionallity unless you know what you are doing:', extra_tags='warning')
    if request.method == 'POST':
        capacity = request.POST.get("capacity")
        requirements = project.getNextReleaseFeatures(capacity)
        if not requirements:
            messages.error(request, 'We wasn\'t able to add any single requirement to the solution because of the lack of capacity:', extra_tags='warning')
    return render(request, 'projects/next_release.html', {'project': project, 'requirements': requirements, 'bad_assesments': zero_assessments, 'bad_influencies': zero_influencies, 'incomplete':incomplete, })

def manual_solution(request, project_id):
    project = Project.objects.all().get(id=project_id)
    requirements = Requirement.objects.all().filter(project=project)

    incomplete, zero_influencies, zero_assessments = project.checkFillables()
    incomplete, zero_influencies, zero_assessments = project.checkFillables()
    if request.method != 'POST' and incomplete:
        messages.error(request, 'We have detected that there is lack of the following data, please, complete those before using this functionallity unless you know what you are doing:', extra_tags='warning')

    if request.method == 'POST':
        # Aqui revisamos el estado de cada checkbox en el formulario por cada requirement que hemos pasado a render
        pass
    return render(request, 'projects/manual_solution.html', {'requirements':requirements, 'project':project, 'bad_assesments': zero_assessments, 'bad_influencies': zero_influencies, 'incomplete':incomplete, })
