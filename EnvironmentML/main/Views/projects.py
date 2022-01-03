from django.shortcuts import render, redirect
from ..models import Project


def projects(request):
    projects = Project.objects.all()
    for i in range(30):
        projects.append(projects[0])
    return render(request=request, template_name="main/projects.html", context={"projects": projects})
