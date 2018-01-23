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
    def satifaction(self):
        totalSatifaction = 0
        for client in self.project.stakeholders.all():
            power = client.power_set.all().get(project=self.project.id)
            assesment = self.assessment_set.all().get(client=client.id)
            totalSatifaction = totalSatifaction + (power.weight * assesment.value)
        return totalSatifaction

    @property
    def productivity(self):
        if self.effort:
            return (self.satifaction//self.effort)
        return 0

    @property
    def contribution(self):
        contributions = {}
        for client in self.project.stakeholders.all():
            contributions[client.name] = self.assessment_set.all().get(client=client.id, requirement=self.id).contribution
        return contributions


class Assessment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    requirement = models.ForeignKey("Requirement", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.client.name + " assessment of requirement: " + self.requirement.name

    @property
    def contribution(self):
        if self.requirement.satifaction:
            power = self.client.power_set.all().get(project=self.requirement.project.id)
            return (power.weight * self.value) / self.requirement.satifaction
        return 0

class GeneralRequirement(models.Model):
    effort = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User')
    description = models.TextField()
    projects = models.ManyToManyField('projects.Project')
