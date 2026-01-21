from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from project.models import Project


# Create your views here.

@login_required
def index(request):
    projects = Project.objects.filter(user=request.user)
    context = {
        projects: projects
    }
    return render(request, 'project/index.html', context)

@login_required
def create(request):
    context = {
    }
    return render(request, 'project/create.html', context)

@login_required
def single(request ,pk):
    context = {
    }
    return render(request, 'project/single.html', context)