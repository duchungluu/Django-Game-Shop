from django.template.loader import render_to_string
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from webshop.models import Game
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from hashlib import md5
import urllib

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

def buy(request, gameID=-1):
    # Returns 404 if Game is not found
    game = get_object_or_404(Game, pk=gameID)

    pid = 'payment_1'
    sid = 'DreamerTeam'
    secret_key = '5102fe96cdd9e062cee5f035e7ec988b'

    # Form checksum
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(
        pid, sid, game.price, secret_key)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()

    # NOTE: ask about this in exercises!
    # Also, is reading & rendering the response the expected way (no css)?
    # - Teemu
    success_url = 'http://localhost:8000/this/does/not/seem/to/matter/success/'
    cancel_url = 'http://localhost:8000/this/does/not/seem/to/matter/cancel/'
    error_url = 'http://localhost:8000/this/does/not/seem/to/matter/error/'

    post_data = [
        ('pid', pid),
        ('sid', sid),
        ('amount', game.price),
        ('success_url', success_url),
        ('cancel_url', cancel_url),
        ('error_url', error_url),
        ('checksum', checksum),
    ]

    # Encode data, execute POST, read response
    data = urllib.parse.urlencode(post_data).encode('UTF-8')
    url = urllib.request.Request('http://payments.webcourse.niksula.hut.fi/pay/', data)
    response = urllib.request.urlopen(url).read()

    return HttpResponse(response)

def buy_success(request):
    return render_to_response('registration/buy_success.html')

def buy_cancel(request):
    return render_to_response('registration/buy_cancel.html')

def buy_error(request):
    return render_to_response('registration/buy_error.html')
