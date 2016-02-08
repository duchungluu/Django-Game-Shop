from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    url = models.URLField()
    published = models.DateTimeField('date published')
    description = models.TextField()
    developer = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='developed_games', unique=False,
        limit_choices_to= {'groups__pk': 1})

    def __str__(self):
        return "{} ({})".format(self.name, self.price)

class Transaction(models.Model):

    game = models.ForeignKey(Game)
    buyer = models.ForeignKey(User, related_name='bought_games')
    state = models.CharField(blank=True, max_length=200)
    buy_started = models.DateTimeField(default=datetime.datetime.now, blank=True)
    buy_completed = models.DateTimeField(null=True)

    def __str__(self):
        return "{}: {}".format(self.buyer, self.game)

class Developer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game, related_name='developers')

class Customer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game, related_name='customers')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'
