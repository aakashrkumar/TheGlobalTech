from django.shortcuts import render, redirect
from ..models import Project


def projects(request):
    return render(request=request, template_name="main/projects.html", context={"projects": Project.objects.all()})
