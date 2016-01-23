from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    url = models.URLField()
    published = models.DateTimeField('date published')
    description = models.TextField()

    class Meta:
        permissions = (
            ("buy_game", "Can buy games"),
        )

    def __str__(self):
        return "{} ({})".format(self.name, self.price)

class Developer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game, related_name='developers')

class Customer(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game, related_name='customers')
