"""dreamerteam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/register/$', 'webshop.views.register_user', name='register'),
    url(r'^accounts/register_success/$', 'webshop.views.register_success'),
    url(r'^accounts/confirm/(?P<activation_key>\w+)/', ('webshop.views.register_confirm')),
    url(r'^accounts/custom_login/$',  'webshop.views.custom_login', name='custom_login'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('webshop.urls')),

]
