from django.test import TestCase, Client
from django.utils import timezone
from django.core import mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from webshop.forms import RegistrationForm, GameForm
from webshop.models import *

class TemplateTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        devGroup = Group.objects.create(name='Developer')
        cusGroup = Group.objects.create(name='Customer')

        userDeveloper = User.objects.create_user('developer',
            'developer@gmail.com', 'developer')
        userCustomer = User.objects.create_user('customer',
            'customer@gmail.com', 'customer')

        devProfile = UserProfile.objects.create(user=userDeveloper,
            isDeveloper = True, username = 'developer')
        UserProfile.objects.create(user=userCustomer,
            isDeveloper = False, username = 'customer')

        Game.objects.create(name = 'Test Game',
        price = 0.99, url = 'www.google.fi', published = timezone.now(),
        description = 'Test Description', developer = devProfile)

        devGroup.user_set.add(userDeveloper)
        cusGroup.user_set.add(userCustomer)

    def testLogin(self):
        """ Check that temp users work """

        self.client.login(username='developer', password='developer')
        devUser = User.objects.get(username='developer')
        profile = UserProfile.objects.get(user=devUser)
        print ('\nDeveloper correctly set up:',end=" ")
        print (profile.isDeveloper)
        self.client.logout()

    def testInvalidUrls(self):
        """ Test for invalid urls """
        print ('Testing invalid urls')

        res = self.client.get('/game/xx')
        self.assertEquals(res.status_code, 404, "Requesting a game page with an invalid code.")

        res = self.client.get('/dev/xx')
        self.assertEquals(res.status_code, 404, "Requesting a developer page with an invalid code.")

        res = self.client.get('/dev/game/xx')
        self.assertEquals(res.status_code, 404, "Requesting a game editing page with an invalid code.")

        res = self.client.get('/xx')
        self.assertEquals(res.status_code, 404, "Requesting a page with an invalid code.")

    def testGameMenu(self):
        """ Tests that the game list is rendered correctly """
        print('Testing gamelist')

        all_games = ({'name': 'testGame', 'description': 'testScription', 'price' : 0.99},
        {'name': 'bestGame', 'description': 'badScription', 'price' : 1.99})
        ren = render_to_string("webshop/gamelist.html", {'all_games': all_games})
        for game in all_games:
            self.assertTrue(ren.find(game['name']) > -1,
            "Testing if the rendered menu contains correct game name")
            self.assertTrue(ren.find(game['description']) > -1,
            "Testing if the rendered menu contains correct game description")
            self.assertTrue(ren.find(str(game['price'])) > -1,
            "Testing if the rendered menu contains correct game price")


    def testBuyGame(self):
        """ Test buying game by accessing /buy/success """
        print('\nTesting access to /buy/success')

        # No user
        self.client.logout()
        res = self.client.get('/buy/success/1')
        self.assertTemplateUsed(res, 'webshop/buy_error.html')

        # With user
        self.client.login(username='customer', password='customer')
        res = self.client.get('/buy/success/1')
        self.assertTemplateUsed(res, 'webshop/buy_error.html')
        self.client.logout()
