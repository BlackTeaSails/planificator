from django.shortcuts import render

def add_project(request):
    return render(request, 'main/team.html', {})

def edit_project(request, project_id):
    return render(request, 'main/team.html', {})

def edit_requirement(request, requirement_id):
    return render(request, 'main/team.html', {})

def remove_project(request, project_id):
    return render(request, 'main/team.html', {})

def projects_list(request, page_number):
    return render(request, 'main/team.html', {})

def users_projects(request, user_id, page_number):
    return render(request, 'main/team.html', {})
