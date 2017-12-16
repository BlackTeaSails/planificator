from django.shortcuts import render, redirect
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.contrib import messages # error and success messages
from django import forms

from clients.models import Client
from .models import Project
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
            project.save()
            messages.success(request, 'Proyecto: '+ project.name +' was added.')
            return redirect("/projects/page-1/")
    return render(request, 'projects/new_project.html', {'form': form,})

def edit_project(request, project_id):
    return render(request, 'projects/projects_list.html', {})

def edit_requirement(request, requirement_id):
    return render(request, 'projects/projects_list.html', {})

def remove_project(request, project_id):
    return render(request, 'projects/projects_list.html', {})

def projects_list(request, page_number):
    prefix = '/projects/page-'
    projects = Project.objects.filter(owner = request.user.id).order_by('creation_date')
    paginator = Paginator(projects, 5)
    last_page = int(paginator.num_pages)
    projects = paginator.page(page_number)
    # si page_number > last_page toma o last_page == 0, toma 404
    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'projects/projects_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'projects':projects})

def users_projects(request, user_id, page_number):
    return render(request, 'projects/projects_list.html', {})
