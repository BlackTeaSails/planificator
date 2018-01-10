from django.contrib import admin
from .models import Requirement, Assessment, GeneralRequirement


admin.site.register(Requirement)
admin.site.register(GeneralRequirement)
admin.site.register(Assessment)
