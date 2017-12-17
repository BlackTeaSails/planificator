from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('auth.User')
    creation_date = models.DateTimeField(default=timezone.now)

    stakeholders = models.ManyToManyField('clients.Client')

    def __str__(self):
        return self.name

    def getNextReleaseFeatures(self, capacity):

        pass

class Requirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey('Project')
    models.ManyToManyField('clients.Client', through='Assessment')
    is_done = models.BooleanField(default=False)

class Assessment(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    value = models.IntegerField()

class GeneralRequirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    projects = models.ManyToManyField('Project')
