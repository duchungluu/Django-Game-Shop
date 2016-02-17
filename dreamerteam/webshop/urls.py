from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/save/$', views.game_save, name='games_save'),
    url(r'^games/load/$', views.game_load, name='games_load'),
    url(r'^games/highscore/$', views.game_highscore, name='games_highscore'),
    url(r'^games$', views.games, name='games'),
    url(r'^buy/(?P<gameID>\d+)?/?$', views.buy, name='buy'),
    url(r'^game/(?P<gameID>\d+)?/?$', views.game, name='game'),
    url(r'^buy/success/(\d+)/$', views.buy_success),
    url(r'^buy/cancel/(\d+)/$', views.buy_cancel),
    url(r'^buy/error/(\d+)/$', views.buy_error),
    url(r'^dev/$', views.dev, name='dev'),
    url(r'^dev/game/(?P<gameID>\d+)/$', views.edit_game, name='edit_game'),
    url(r'^dev/game/add/', views.add_game, name='add_game'),
    url(r'^buy/success/', views.buy_success),
    url(r'^buy/cancel/', views.buy_cancel),
    url(r'^buy/error/', views.buy_error),
]
