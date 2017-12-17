from django import template

from projects.models import Project

register = template.Library()

@register.filter
def getweight(powers, project_id):
    power = powers.all().get(project=project_id)
    return power.weight
