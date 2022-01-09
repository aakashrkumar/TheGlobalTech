import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Project


def projects(request):
    projectsList = list(Project.objects.all().order_by('-project_date'))
    for i in range(30):
        projectsList.extend(projectsList)
        if len(projectsList) > 30:
            break
    random.shuffle(projectsList)
    return render(request=request, template_name="main/projects.html", context={"projects": projectsList})


def projectRender(request, project):
    return render(request=request, template_name="main/project.html", context={"project": project})


def projectslug(request, slug):
    projectsList = list(Project.objects.all().order_by('-project_date').filter(slug=slug))
    if len(projectsList) > 0:
        return projectRender(request, projectsList[0])
    return HttpResponse(status=404)
