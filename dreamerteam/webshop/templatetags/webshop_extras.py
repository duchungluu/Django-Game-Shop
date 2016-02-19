from django.contrib.auth.models import Group
from django import template

register = template.Library()

@register.filter
def is_developer(user):
    return user.groups.filter(name="Developer").exists()
