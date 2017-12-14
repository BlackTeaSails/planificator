from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', views.reglog_view, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.reglog_view, name='signup'),
    url(r'^recover/$', views.recover_view, name='recover'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^edit/(?:user-(?P<user_id>\d+)/)$', views.modify_user, name='modify_user'),
    url(r'^remove/(?:user-(?P<user_id>\d+)/)$', views.remove_user, name='remove_user'),
    url(r'^users/(?:page-(?P<page_number>\d+)/)$', views.user_list, name='users_list'),
    url(r'^change_pass/$', views.change_pass, name='change_pass'),
]
