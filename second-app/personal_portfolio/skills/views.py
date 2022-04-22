from django.shortcuts import render
from .models import Skills


def index(request):
    project = Skills.objects.all()
    return render(request, 'skills/index.html', {'projects': project})
