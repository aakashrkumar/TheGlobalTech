from django.shortcuts import render
from django.contrib.auth.models import User


def aboutus(request):
    team = User.objects.all().filter(is_staff=True)
    return render(request, 'aboutus.html', context={'team': team})
