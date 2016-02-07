from django.http import *
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django import forms
import urllib, hashlib, datetime, random
from webshop.models import *
from webshop.forms import RegistrationForm, GameForm
from django.conf import settings

def index(request):

    context = {
        "all_games": Game.objects.all()
    }

    target = "webshop/index.html"

    return render(request, target, context)

def games(request):
    # iiro ajax call for search functionality - not very stylish here, but 1 version! :)

    if request.method == 'GET':

        searched_games = None

        if request.GET.get('search_term'):
            searched_games = Game.objects.filter(name__icontains=request.GET.get('search_term'))

        if request.GET.get('order'):
            searched_games = searched_games.extra(order_by = [request.GET.get('order')])

        if request.is_ajax():
            html = render_to_string( 'webshop/gamelist.html', {'all_games': searched_games})
            return HttpResponse(html)

        if searched_games is not None:
            context = {
                "all_games": searched_games
            }
        else:
            context = {
                "all_games": Game.objects.all()
            }

        target = "webshop/games.html"

        return render(request, target, context)

def register_user(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #adding user to specific group
            role = request.POST.get('group')
            g = Group.objects.get(name=role)
            g.user_set.add(user)

            #preparing activaion email
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)

            return HttpResponseRedirect("/accounts/register_success")


    args = {}
    args.update(csrf(request))
    #assigning custom form
    args['form'] = RegistrationForm()
    print (args)
    return render_to_response('registration/register.html' , args)

def register_success(request):
    return render_to_response('registration/register_success.html')

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('registration/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('registration/confirm.html')

def custom_login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return HttpResponseRedirect(reverse('login'))

def buy(request, gameID=-1):
    # Returns 404 if Game is not found
    game = get_object_or_404(Game, pk=gameID)

    # Create Transaction
    t = Transaction(game=game, buyer=request.user)
    t.save()

    pid = str(t.id)
    sid = 'DreamerTeam'

    # Form checksum and save to model
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(
        pid, sid, game.price, settings.PAYMENT_KEY)
    checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()

    domain = 'http://' + request.META['HTTP_HOST']
    success_url = domain + '/buy/success/'
    cancel_url = domain + '/buy/cancel/'
    error_url = domain + '/buy/error/'

    post_data = [
        ('pid', pid),
        ('sid', sid),
        ('amount', game.price),
        ('success_url', success_url),
        ('cancel_url', cancel_url),
        ('error_url', error_url),
        ('checksum', checksum),
    ]

    # Send form from javascript
    data = urllib.parse.urlencode(post_data).encode('UTF-8')
    return render_to_response('webshop/buygame.html', {'post_data': data})

def buy_success(request):
    pid = request.GET.get('pid')
    ref = request.GET.get('ref')
    result = request.GET.get('result')
    receivedChecksum = request.GET.get('checksum')

    ourChecksum = "pid={}&ref={}&result={}&token={}".format(
        pid, ref, result, settings.PAYMENT_KEY)
    ourChecksum = hashlib.md5(ourChecksum.encode("ascii")).hexdigest()

    if (receivedChecksum == ourChecksum):

        # Update database
        t = Transaction.objects.get(pk=pid)
        t.state = result
        t.buy_completed = timezone.now()
        t.save()
        return render_to_response('webshop/buy_success.html')
    else:
        return HttpResponseRedirect("/")

def buy_cancel(request):
    pid = request.GET.get('pid')
    result = request.GET.get('result')
    t = Transaction.objects.get(pk=pid)
    t.state = result
    t.save()
    return render_to_response('webshop/buy_cancel.html')

def buy_error(request):
    pid = request.GET.get('pid')
    result = request.GET.get('result')
    t = Transaction.objects.get(pk=pid)
    t.state = result
    t.save()
    return render_to_response('webshop/buy_error.html')

def game(request, gameID = None):
    context = {}
    game = get_object_or_404(Game, pk=gameID)
    if gameID:
        context["game"] = game
    return render(request, "webshop/game.html", context)

def dev(request):
    user = request.user
    if user.is_authenticated():
        if(user_has_group(user, 'developer')):
            context = {
                "all_games": Game.objects.all() # should query all games where user is developer
            }
            return render(request, "webshop/dev.html", context)
    return render(request, "webshop/home.html")

def edit_game(request, gameID = None):
    game = get_object_or_404(Game, pk=gameID)
    form = GameForm(request.POST or None, instance=game)

    if request.method == 'POST':
        if form.is_valid():
            game = form.save()
            return HttpResponseRedirect('/dev/')
    return render(request, "webshop/game_edit.html", {'form': form})

def user_has_group(user,groupname):
    for group in user.groups.all():
        if group.name.lower() == groupname.lower(): # case insensitive
            return True
    return False
