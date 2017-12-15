from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^add_client/$', views.add_client, name='login'),
    url(r'^edit/(?:client-(?P<client_id>\d+)/)$', views.edit_client, name='edit_client'),
    url(r'^(?:page-(?P<page_number>\d+)/)$', views.client_list, name='users_list'),
]
