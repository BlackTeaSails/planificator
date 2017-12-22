from django.contrib import admin
from .models import Project, Requirement, Power, Assessment


admin.site.register(Project)
admin.site.register(Requirement)
admin.site.register(Power)
admin.site.register(Assessment)
