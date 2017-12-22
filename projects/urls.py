from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^detail/(?:project-(?P<project_id>\d+)/)$', views.project_detail, name='project_detail'),
    url(r'^edit/(?:project-(?P<project_id>\d+)/)$', views.edit_project, name='edit_project'),
    url(r'^(?:page-(?P<page_number>\d+)/)$', views.projects_list, name='projects_list'),
    url(r'^(?:user-(?P<user_id>\d+)/(?:page-(?P<page_number>\d+))/)$', views.users_projects, name='users_projects'),
    url(r'^remove/(?:project-(?P<project_id>\d+)/)$', views.remove_project, name='remove_project'),
    url(r'^release/(?:project-(?P<project_id>\d+)/)$', views.next_release, name='next_release'),
]
