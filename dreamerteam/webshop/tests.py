from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from webshop.models import *

class TemplateTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def testInvalidUrls(self):
        """ Test for invalid urls """

        res = self.client.get('/game/xx')
        self.assertEquals(res.status_code, 404, "Requesting a game page with an invalid code.")

        res = self.client.get('/dev/xx')
        self.assertEquals(res.status_code, 404, "Requesting a developer page with an invalid code.")

        res = self.client.get('/dev/game/xx')
        self.assertEquals(res.status_code, 404, "Requesting a game editing page with an invalid code.")

        res = self.client.get('/xx')
        self.assertEquals(res.status_code, 404, "Requesting a page with an invalid code.")

    def testContinentMenu(self):
        """ Tests that the game list is rendered correctly """

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

    # Not yet implemented
    # def testPageContents(self):
    #     """ This test requests pages for all games
    #     TODO: Check contents of page """
    #     for game in Game.objects.all():
    #         response = self.client.get('game/' + game.id), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #         self.assertEquals(response.status_code, 200, "Testing request status code.")
