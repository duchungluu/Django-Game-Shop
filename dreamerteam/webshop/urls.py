from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games$', views.games, name='games'),
    url(r'^buy/?(?P<gameID>\d+)?/?$', views.buy, name='buy'),
    url(r'^game/?(?P<gameID>\d+)?/?$', views.game, name='game'),
    url(r'^buy/success/(\d+)/$', views.buy_success),
    url(r'^buy/cancel/(\d+)/$', views.buy_cancel),
    url(r'^buy/error/(\d+)/$', views.buy_error),
    url(r'^dev/$', views.dev),
    url(r'^dev/games/$', views.dev),
    url(r'^dev/games/?(?P<gameID>\d+)/$', views.edit_game),
]
