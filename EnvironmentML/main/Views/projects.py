import random

from django.shortcuts import render, redirect
from ..models import Project


def projects(request):
    projectsList = list(Project.objects.all().order_by('-project_date'))
    for i in range(30):
        projectsList.extend(projectsList)
        if len(projectsList) > 30:
            break
    random.shuffle(projectsList)
    return render(request=request, template_name="main/projects.html", context={"projects": projectsList})
