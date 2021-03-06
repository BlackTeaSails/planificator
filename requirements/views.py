from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages
from django.contrib.auth.models import User


from clients.models import Client
from projects.models import Project
from .models import Requirement, GeneralRequirement, Assessment
from .forms import NewRequirementForm

def list_requirements(request, page_number):
    prefix = '/requirements/page-'
    requirements = GeneralRequirement.objects.filter(owner = request.user.id).order_by('id')
    paginator = Paginator(requirements, 15)
    last_page = int(paginator.num_pages)
    requirements = paginator.page(page_number)

    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'requirements/requirements_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'requirements':requirements})

def new_requirement(request, project_id):
    form = NewRequirementForm()
    if request.method == 'POST':
        form = NewRequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save(commit=False)
            project = Project.objects.all().get(id=project_id)
            requirement.project = project
            requirement.save()
            general = GeneralRequirement(effort=requirement.effort,
                name=requirement.name,
                description=requirement.description,
                owner = User.objects.all().get(id=request.user.id))
            general.save()
            general.projects.add(project)
            general.save()
            for stakeholder in project.stakeholders.all():
                assesment = Assessment(client=stakeholder, requirement=requirement )
                assesment.save()
            requirement.save()
            messages.success(request, 'Requirement: '+ requirement.name +' was created.')
            return redirect('/projects/detail/project-'+ str(requirement.project.id)+'/')
    return render(request, 'requirements/new_requirement.html', {'form':form, })

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
    return render(request, 'requirements/new_requirement.html', {'form':form, 'requirement':requirement, })

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

def remove_general_requirement(request, requirement_id):
    requirement = GeneralRequirement.objects.all().get(id=requirement_id)
    requirement.delete()
    messages.error(request, 'General Requirement: '+ requirement.name +' was deleted', extra_tags='success')
    return redirect('/requirements/page-1/')

def edit_general_requirement(request, requirement_id):
    requirement = GeneralRequirement.objects.get(id=requirement_id)
    form = NewRequirementForm(instance=requirement)
    if request.method == 'POST':
        form = NewRequirementForm(request.POST, instance=requirement)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.save()
            messages.success(request, 'General Requirement: '+ requirement.name +' was modified.')
            return redirect('/requirements/page-1/')
    return render(request, 'requirements/new_requirement.html', {'form':form, 'requirement':requirement})

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

def reuse_requirement(request, project_id, page_number):
    prefix = '/requirements/reuse_requirement/project-'+str(project_id)+'/page-'
    project = Project.objects.get(id=project_id)
    requirements = GeneralRequirement.objects.filter(owner = request.user.id)
    paginator = Paginator(requirements, 15)
    last_page = int(paginator.num_pages)
    requirements = paginator.page(page_number)

    pages = calculate_pages(int(page_number), last_page)
    if request.method == 'POST':
        effort = request.POST.get('effort')
        gen_requirement = GeneralRequirement.objects.get(id = request.POST.get('requirement_id'))
        
        actual_req = Requirement.objects.create(project=project)
        actual_req.name = gen_requirement.name
        actual_req.description = gen_requirement.description
        actual_req.effort = effort

        gen_requirement.projects.add(project)
        gen_requirement.save()

        for stakeholder in project.stakeholders.all():
            assesment = Assessment(client=stakeholder, requirement=actual_req )
            assesment.save()
        # resto de los datos del requisito
        actual_req.save()
        messages.success(request, gen_requirement.name + ' - requirement was reused in project:' + project.name)
    return render(request, 'requirements/reuse_requirement.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'project':project, 'requirements':requirements})
