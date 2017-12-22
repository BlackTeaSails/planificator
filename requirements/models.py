from django.db import models

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey('projects.Project')
    effort = models.IntegerField(default=0)
    assessments = models.ManyToManyField('clients.Client', through='Assessment')
    state = models.BooleanField(default=False)
    last_released = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def benefit(self):
        totalBenefit = 0
        for client in self.project.stakeholders.all():
            power = client.power_set.all().get(project=self.project.id)
            assesment = self.assessment_set.all().get(client=client.id)
            totalBenefit = totalBenefit + (power.weight * assesment.value)
        return (totalBenefit//self.effort)

class Assessment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    requirement = models.ForeignKey("Requirement", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.client.name + " assessment of requirement: " + self.requirement.name

class GeneralRequirement(models.Model):
    effort = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    projects = models.ManyToManyField('projects.Project')
