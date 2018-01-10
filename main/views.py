from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html', {})

def team_view(request):
    return render(request, 'main/team.html', {})

def manual_view(request):
    return render(request, 'main/manual.html', {})
