from django.shortcuts import render, redirect

from ..models import Project


def homepage(request):
    projectsList = list(Project.objects.all().order_by('-project_date'))
    return render(request=request, template_name="main/home.html", context={'projects': projectsList})
