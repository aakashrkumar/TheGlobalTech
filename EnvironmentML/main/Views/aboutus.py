from django.shortcuts import render
from django.contrib.auth.models import User
from django import template

register = template.Library()


@register.filter
def spaceUnderscore(value):
    return value.replace(" ", "_")


def aboutus(request):
    team = User.objects.all().filter(is_staff=True)
    return render(request, 'main/aboutus.html', context={'team': team})


def teamslug(request, slug):
    team = User.objects.all().filter(is_staff=True)
    author = User.objects.get(username=slug.replace('_', ' '))
    return render(request, 'main/authors.html', context={'team': team, 'author': author})
