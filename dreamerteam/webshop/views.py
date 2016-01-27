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
from webshop.forms import RegistrationForm

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

    pid = 'payment_1'
    sid = 'DreamerTeam'
    secret_key = '5102fe96cdd9e062cee5f035e7ec988b'

    # Form checksum
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(
        pid, sid, game.price, secret_key)
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
    return render_to_response('webshop/buy_success.html')

def buy_cancel(request):
    return render_to_response('webshop/buy_cancel.html')

def buy_error(request):
    return render_to_response('webshop/buy_error.html')

def game(request, gameID = None):
    context = {}
    game = get_object_or_404(Game, pk=gameID)
    if gameID:
        context["game"] = game
    return render(request, "webshop/game.html", context)
