from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages

from clients.models import Client
from projects.models import Project
from .models import Requirement, GeneralRequirement, Assessment
from .forms import NewRequirementForm

#Falta listar requisitos generales
def list_requirements(request, page_number):
    return render(request, 'main/team.html', {})

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

def remove_requirement(request, requirement_id):
    requirement = Requirement.objects.all().get(id=requirement_id)
    requirement.delete()
    messages.error(request, 'Requirement: '+ requirement.name +' was deleted from the project.', extra_tags='success')
    return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')

def assessments(request, requirement_id):
    requirement = Requirement.objects.all().get(id=requirement_id)
    if request.method == 'POST':
        for client in requirement.project.stakeholders.all():
            assessment = Assessment.objects.all().get(client=client.id, requirement=requirement_id)
            assessment.value = request.POST.get("value-client-"+str(client.id))
            assessment.save()
        messages.success(request, 'Clients\' assessments:  were saved')
        return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')
    return render(request, 'requirements/assessments.html', {'requirement':requirement})
