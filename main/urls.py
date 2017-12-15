from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^team/', views.team_view, name='team'),
    url(r'^', views.index, name='index'),
]
