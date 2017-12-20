from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('auth.User')
    creation_date = models.DateTimeField(default=timezone.now)

    stakeholders = models.ManyToManyField('clients.Client', through='Power')

    def __str__(self):
        return self.name

    def getNextReleaseFeatures(self, capacity):
        sortedRequirements = sorted(Requirement.objects.all().filter(project=self).filter(state=False), key=lambda t: t.benefit)
        requirementsRelease = []
        sum=0
        for requirement in sortedRequirements:
            if (sum + requirement.effort <=int(capacity)):
                sum = sum + requirement.effort
                requirementsRelease.append(requirement.id)
        return Requirement.objects.filter(id__in=requirementsRelease)

class Power(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.client.name+" weight in project"+self.project.name

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey('Project')
    effort = models.IntegerField(default=0)
    assessments = models.ManyToManyField('clients.Client', through='projects.Assessment')
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def benefit(self):
        totalBenefit = 0
        for client in self.project.stakeholders.all():
            power = client.power_set.all().get(project=self.project.id)
            assesment = self.assessment_set.all().get(client=client.id)
            totalBenefit = totalBenefit + (power.weight * assesment.value)
        return totalBenefit

class Assessment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.client.name + " assessment of requirement: " + self.requirement.name

class GeneralRequirement(models.Model):
    effort = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    projects = models.ManyToManyField('Project')
