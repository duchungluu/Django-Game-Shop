from django.template.loader import render_to_string
from django.shortcuts import render, render_to_response 
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from webshop.models import Game
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf

def index(request):

    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/index.html"

    return render(request, target, context)

def games(request):
    # iiro ajax call for search functionality - not very stylish here, but 1 version! :) 
    if request.is_ajax(): 
        if request.method == 'GET':
            search_term = request.GET['search_term']
            searched_games = Game.objects.filter(name__icontains=search_term)
            
            html = render_to_string( 'webshop/gamelist.html', {'all_games': searched_games})

            return HttpResponse(html)
    
    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/games.html"

    return render(request, target, context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/register_success")

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()
    print (args)
    return render_to_response('registration/register.html' , args)

def register_success(request):
    return render_to_response('registration/register_success.html')

