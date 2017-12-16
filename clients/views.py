from django.shortcuts import render, redirect
from django.contrib import messages # error and success messages
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page
from django.http import HttpResponseRedirect

from .models import Client
from .forms import NewClientForm

def add_client(request):
    form = NewClientForm()
    if request.method == 'POST':
        form = NewClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            messages.success(request, 'Cliente: '+client.name+' was added.')
            return redirect("/clients/page-1/")
    return render(request, 'clients/new_client.html', {'form': form,})

def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    form = NewClientForm(instance=client)
    if request.method == 'POST':
        form = NewClientForm(request.POST, instance=Client.objects.get(id=client_id))
        if form.is_valid():
            form.save()
            messages.success(request, client.name+' data were refreshed.')
            return redirect("/clients/page-1/")
    return render(request, 'clients/edit_client.html', {'form': form, 'client': client})

def client_list(request, page_number):
    prefix = '/clients/page-'
    clients = Client.objects.filter(owner = request.user.id).order_by('id')
    paginator = Paginator(clients, 4)
    last_page = int(paginator.num_pages)
    clients = paginator.page(page_number)
    # si page_number > last_page toma o last_page == 0, toma 404
    pages = calculate_pages(int(page_number), last_page)
    print(pages)
    return render(request, 'clients/clients_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'prefix':prefix, 'clients':clients})
