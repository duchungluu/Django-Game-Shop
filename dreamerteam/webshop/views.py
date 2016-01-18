from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from webshop.models import Game
from django import forms
from django.contrib.auth.forms import UserCreationForm


def index(request):

    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/index.html"

    return render(request, target, context)

def games(request):

    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/gamelist.html"

    return render(request, target, context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
