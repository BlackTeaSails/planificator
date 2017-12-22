from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    charge = models.TextField()
    owner = models.ForeignKey('auth.User')
    assessments = models.ManyToManyField('clients.Client', through='requirements.Assessment')
    projects = models.ManyToManyField('projects.Project', through='projects.Power')

    def __str__(self):
        return self.name
