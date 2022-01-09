from django.shortcuts import render
from django.contrib.auth.models import User


def aboutus(request):
    team = User.objects.all().filter(is_staff=True)
    return render(request, 'main/aboutus.html', context={'team': team})
