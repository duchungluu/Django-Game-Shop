from django.http import *
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django import forms
import urllib, hashlib, datetime, random
from webshop.models import *
from webshop.forms import *
from django.conf import settings
from django.db.models import Max, F
import json
from django.core import serializers


def index(request):

    # Redirect non-logged in visitors to /games
    if not request.user.is_authenticated():
        return redirect('games')

    context = {
        "all_games": user_owned_games(request.user),
        "games_are_owned": True
    }

    target = "webshop/index.html"

    return render(request, target, context)


def games(request):

    if request.method == 'GET':

        searched_games = Game.objects.all()

        if request.GET.get('search_term'):
            searched_games = searched_games.filter(name__icontains=request.GET.get('search_term'))

        if request.GET.get('order'):
            searched_games = searched_games.extra(order_by = [request.GET.get('order')])

        # Filter out owned games if user is logged in
        if request.user.is_authenticated():
            owned_games = user_owned_games(request.user)
            if owned_games is not None:
                searched_games = searched_games.exclude(
                    id__in=[g.id for g in owned_games])

        if request.is_ajax():
            html = render_to_string('webshop/gamelist.html', {'all_games': searched_games, 'games_are_owned': 'False'})
            return HttpResponse(html)

        context = {
            "all_games": searched_games,
            "games_are_owned": False
        }

        target = "webshop/games.html"
        return render(request, target, context)

def register_user(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password1 = form.cleaned_data['password1']
            user = User(first_name=first_name,
            last_name = last_name,username=username,
            password = password1, email=email)
            role = request.POST.get('group')

            #preparing activaion email
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            #adding user to specific group
            g = Group.objects.get(name=role)
            g.user_set.add(user)

            if (role == 'Developer'):
                user.isDeveloper = True
            else:
                user.isDeveloper = False

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires,isDeveloper = user.isDeveloper,username = username )
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://dreamerteam.herokuapp.com/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)

            p = UserProfile.objects.get(username=username)
            #do something with user objects, such asL user.is_active = True
            user.save()
            return HttpResponseRedirect("/accounts/register_success")


    args = {}
    args.update(csrf(request))
    #assigning custom form
    args['form'] = RegistrationForm()
    return render(request, 'registration/register.html' , args)

def register_success(request):
    return render(request, 'registration/register_success.html')

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render(request, 'registration/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render(request, 'registration/confirm.html')

def custom_login(request):
    form = AuthenticationForm(request.POST or None)
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                messages.error(request, 'Your account is inactive')
        else:
            messages.error(request, 'Wrong username or password')
    return render(request, 'registration/login.html', {'form': form })

def buy(request, gameID=-1):
    # Returns 404 if objects are not found
    game = get_object_or_404(Game, pk=gameID)
    userProfile = get_object_or_404(UserProfile, user=request.user)

    # If user already owns the game, redirect to game page as a failsafe
    if Transaction.objects.filter(game=game, buyer=userProfile, state='success'):
        return redirect('game', gameID=game.id)

    # Create Transaction
    t = Transaction(game=game, buyer=userProfile)
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
    return render(request, 'webshop/buygame.html', {'post_data': data} )

def buy_success(request):
    pid = request.GET.get('pid')
    ref = request.GET.get('ref')
    result = request.GET.get('result')
    receivedChecksum = request.GET.get('checksum')

    ourChecksum = "pid={}&ref={}&result={}&token={}".format(
        pid, ref, result, settings.PAYMENT_KEY)
    ourChecksum = hashlib.md5(ourChecksum.encode("ascii")).hexdigest()

    if (receivedChecksum == ourChecksum):
        # Update Transaction and increment Game's total_bought
        try:
            t = Transaction.objects.get(pk=pid)
            t.state = result
            t.buy_completed = timezone.now()
            t.save()
            Game.objects.filter(pk=t.game.id).update(total_bought=F("total_bought") + 1)
        except:
            return render(request, 'webshop/buy_finished.html')

    return render(request, 'webshop/buy_finished.html', {'state': result})

def buy_error(request):
    try:
        pid = request.GET.get('pid')
        result = request.GET.get('result')
        t = Transaction.objects.get(pk=pid)
        t.state = result
        t.save()
        return render(request, 'webshop/buy_finished.html', {'state': result})
    except:
        return render(request, 'webshop/buy_finished.html')

def game(request, gameID = None):
    context = {}
    isBought = False;

    #check if the id of the game is right  (id exists)
    try:
        game = Game.objects.get(pk=gameID)
    except:
        return render(request, "webshop/game_wrongid.html")

    user = request.user
    if user.is_authenticated():
        user_profile = get_userprofile(user)
        context["user"] = user

        #check if the user owns the game
        try:
            transactions = Transaction.objects.get(buyer = user_profile,
            state="success", game =game)
            isBought = True;
        except:
            pass

        # Get top-10 scores for the game
        top10 = GameData.objects.filter(gameID=gameID).order_by('-highScore')[:10]
        context["top_10"] = top10

    if gameID:
        context["game"] = game
    context["isBought"] = isBought;
    return render(request, "webshop/game.html", context)

def dev(request):
    user = request.user
    if not user_is_developer(user):
         raise PermissionDenied

    # All games where user is developer
    userProfile = get_userprofile(user)
    games = userProfile.developed_games.all()

    # 10 most recent transactions related to developer's games
    transactions = Transaction.objects.filter(game__in=games,
    state='success').order_by('-buy_completed')[:10]

    context = {
        "games": games,
        "transactions" : transactions
    }
    return render(request, "webshop/dev.html", context)

def edit_game(request, gameID = None):
    if not user_is_developer(request.user):
         raise PermissionDenied

    game = get_object_or_404(Game, pk=gameID)
    form = GameForm(request.POST or None, instance=game)

    if request.method == 'POST':
        if request.POST.get('submit') == 'Submit':
            if form.is_valid():
                game = form.save()
                return HttpResponseRedirect('/dev/')

        if request.POST.get('submit') == 'Delete':
            game.delete()
            return HttpResponseRedirect('/dev/')

    return render(request, "webshop/game_edit.html", {'form': form})

def add_game(request):
    if not user_is_developer(request.user):
         raise PermissionDenied

    game = Game()
    form = GameForm(request.POST or None, instance=game)

    if request.method == 'POST':
        if form.is_valid():
            game = form.save(commit = False)
            game.developer = get_userprofile(request.user)
            game.save()
            return HttpResponseRedirect('/dev/')

    return render(request, "webshop/game_add.html", {'form':form})


def get_userprofile(user):
    try:
        return UserProfile.objects.get(user=user)
    except:
        return None

def user_has_group(user, groupname):
    for group in user.groups.all():
        if group.name.lower() == groupname.lower(): # case insensitive
            return True

    return False

def user_is_developer(user):
    if user.is_authenticated():
        user_profile = get_userprofile(user)
        if not user_profile is None:
            return user_profile.isDeveloper

    return False

def user_owned_games(user):
    userProfile = get_userprofile(user)
    try:
        transactions = userProfile.bought_games.filter(state='success')
        games = []
        for t in transactions:
            games.append(t.game)
        return games
    except:
        return None

def game_save(request):
    if request.POST:
        gameID = request.POST['gameID']
        username = request.POST['username']
        json_text = request.POST['json_text']
        try:
            gameData = GameData.objects.get(gameID = gameID,
            username = username)
            gameData.gameStatus = json_text;
            gameData.save()
        except :
            gameData = GameData (gameID = gameID, username = username,
            gameStatus = json_text)
            gameData.save()

    return HttpResponse("data saved!")

def game_load(request):
    if request.POST:
        gameID = request.POST['gameID']
        username = request.POST['username']
        gameData = GameData.objects.get(username=username, gameID = gameID)
        jsonString = gameData.gameStatus
    return HttpResponse(jsonString)

def game_highscore_set(request):
    if request.POST:
        gameID = request.POST['gameID']
        username = request.POST['username']
        score = request.POST['score']
        try:
            gameData = GameData.objects.get(username=username, gameID = gameID)
            highScore = gameData.highScore
            if (int(score) > highScore):
                gameData.highScore = int(score)
                gameData.save()
        except :
            gameData = GameData (gameID = gameID, username = username,
            highScore = int(score))
        gameData.save()
        return HttpResponse("score entered to the system")


def game_highscore_get(request,gameID = -1):
    if request.POST:

        username = request.POST['username']

        result  = {}
        try:
            gameData = GameData.objects.get(username=username, gameID = gameID)
            highScore = gameData.highScore
            result['highscore'] = highScore
        except:
            pass
        try :
            data = GameData.objects.filter(gameID=gameID).order_by('-highScore')[:10]
            top10 = serializers.serialize("json", data, fields  = ('username','highScore'))
            result["top_10"] = (top10)
        except:
            pass

        return HttpResponse(json.dumps(result), content_type="application/json")


def profile(request):
    if request.user.is_authenticated():
        user = request.user
        form = ProfileForm(instance = user)

        args = {}
        args['form'] = form
        args['user'] = user
        return render(request, 'webshop/profile.html' , args)
    else:
        return HttpResponse("You need to be logged in to access ths page.")

def facebook_complete(request):
    user = request.user
    if user.is_authenticated():
        if not user_has_group(user, 'Developer') and not user_has_group(user, 'Customer'):
            return render(request, "registration/facebook_register.html")
    return HttpResponseRedirect('/')

def register_user_group(request):
    if request.POST:
        user = request.user
        if user.is_authenticated():
            if not user_has_group(user, 'Developer') and not user_has_group(user, 'Customer'):
                role = request.POST.get('group')

                #adding user to specific group
                group = Group.objects.get(name=role)
                group.user_set.add(user)

                if (role == 'Developer'):
                        user.isDeveloper = True
                else:
                    user.isDeveloper = False

                usr_profile = get_userprofile(user)
                email = user.email
                #preparing activation email
                random_string = str(random.random()).encode('utf8')
                salt = hashlib.sha1(random_string).hexdigest()[:5]
                salted = (salt + email).encode('utf8')
                activation_key = hashlib.sha1(salted).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)

                if usr_profile is None:
                    # Create and save user profile
                    new_profile = UserProfile(user=user, activation_key=activation_key,
                    key_expires=key_expires, isDeveloper = user.isDeveloper, username = user.username)
                    new_profile.save()
                else:
                    # update old profile
                    usr_profile.isDeveloper = user.isDeveloper
                    usr_profile.user = user
                    usr_profile.key_expires = key_expires
                    usr_profile.username = user.username
                    usr_profile.activation_key=activation_key
                    usr_profile.save()

                user.save()
                return render(request, "registration/register_success.html")

    return HttpResponseRedirect('/')
