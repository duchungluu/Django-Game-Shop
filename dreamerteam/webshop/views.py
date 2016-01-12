from django.shortcuts import render
from django.http import HttpResponse
from webshop.models import Game

def index(request):

    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/index.html"
    if request.is_ajax():
        target = "webshop/gametable.html"

    return render(request, target, context)
