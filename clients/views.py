from django.shortcuts import render
from .models import Client
from django.core.paginator import Paginator # for paginate the users
from planificator.utils import calculate_pages # extra utility to calculate the surroinding page numbers of the actual page

def add_client(request):
    return render(request, 'clients/new_client.html', {})

def edit_client(request, client_id):
    return render(request, 'clients/new_client.html', {})

def client_list(request, page_number):
    clients = Client.objects.filter(owner = request.user.id).order_by('id')
    paginator = Paginator(clients, 15)
    last_page = int(paginator.num_pages)
    clients = paginator.page(page_number)
    # si page_number > last_page toma o last_page == 0, toma 404
    pages = calculate_pages(int(page_number), last_page)
    return render(request, 'clients/clients_list.html', {'range':pages, 'page':page_number, 'last_page':last_page, 'clients':clients})
