from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all_requirements/(?:page-(?P<page_number>\d+)/)$', views.list_requirements, name='list_requirements'),
    url(r'^new_requirement/(?:project-(?P<project_id>\d+)/)$', views.new_requirement, name='new_requirement'),
    url(r'^edit/(?:requirement-(?P<requirement_id>\d+)/)$', views.edit_requirement, name='edit_requirement'),
    url(r'^toggle/(?:requirement-(?P<requirement_id>\d+)/)$', views.toggle_requirement, name='toggle_requirement'),
    url(r'^remove/(?:requirement-(?P<requirement_id>\d+)/)$', views.remove_requirement, name='remove_requirement'),
    url(r'^assessments/(?:requirement-(?P<requirement_id>\d+)/)$', views.assessments, name='assessments'),
]
