from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games$', views.games, name='games'),
    url(r'^buy/?(?P<gameID>\d+)?/?$', views.buy, name='buy'),
    url(r'^game/?(?P<gameID>\d+)?/?$', views.game, name='game'),
    url(r'^buy/success/', views.buy_success),
    url(r'^buy/cancel/', views.buy_cancel),
    url(r'^buy/error/', views.buy_error),
]
