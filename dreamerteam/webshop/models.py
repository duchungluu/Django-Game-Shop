from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
    isDeveloper = models.BooleanField(default = False)
    username = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural='User profiles'

    def __str__(self):
        return self.user.username


class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    url = models.URLField()
    published = models.DateTimeField('date published')
    description = models.TextField()
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
        related_name='developed_games', unique=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.price)


class Transaction(models.Model):
    game = models.ForeignKey(Game)
    buyer = models.ForeignKey(UserProfile, related_name='bought_games')
    state = models.CharField(blank=True, max_length=200)
    buy_started = models.DateTimeField(default=datetime.datetime.now, blank=True)
    buy_completed = models.DateTimeField(null=True)

    def __str__(self):
        return "{}: {}".format(self.buyer, self.game)


class GameData(models.Model):
    gameID = models.IntegerField()
    username = models.CharField(max_length=100)
    gameStatus = models.TextField()
    highScore = models.IntegerField(default = 0)
    class Meta:
        unique_together = (("gameID", "username"),)
