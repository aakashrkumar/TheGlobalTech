from django.shortcuts import render, redirect


def projects(request):
    return render(request=request, template_name="main/home.html")
