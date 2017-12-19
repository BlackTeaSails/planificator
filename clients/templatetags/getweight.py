from django import template

from projects.models import Project

register = template.Library()

@register.filter
def getweight(powers, project_id):
    power = powers.all().get(project=project_id)
    return power.weight

@register.filter
def getassesstment(assessments, requirement_id):
    assessment = assessments.all().get(requirement=requirement_id)
    return assessment.value
