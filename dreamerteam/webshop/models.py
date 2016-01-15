from django.db import models
from django.contrib.auth.models import Group, User


class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    url = models.URLField()
    published = models.DateTimeField('date published')

    def __str__(self):
        return "{} ({})".format(self.name, self.price)


class Developer(Group):
    ourownname = models.CharField(max_length=50)
