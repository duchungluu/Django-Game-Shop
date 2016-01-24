from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from webshop.models import Game
from webshop.forms import RegistrationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.models import Group


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

    target = "webshop/games.html"

    return render(request, target, context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #adding user to specific group
            role = request.POST.get('part')
            g = Group.objects.get(name=role)
            g.user_set.add(user)
            return HttpResponseRedirect("/accounts/register_success")

    args = {}
    args.update(csrf(request))

    #assigning custom form
    args['form'] = RegistrationForm()
    print (args)
    return render_to_response('registration/register.html' , args)

def register_success(request):
    return render_to_response('registration/register_success.html')
