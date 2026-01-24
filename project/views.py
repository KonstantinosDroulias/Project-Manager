from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required
def index(request):
    projects = Project.objects.filter(user=request.user)
    context = {
        'projects': projects  # Fixed syntax error (added quotes)
    }
    return render(request, 'project/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')  # Make sure your URL name for index is 'home'
    else:
        form = ProjectForm()

    context = {
        'form': form
    }
    return render(request, 'project/create.html', context)


@login_required
def single(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)

    if request.method == 'POST':
        if 'delete' in request.POST:
            project.delete()
            return redirect('home')

        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('single-project', pk=pk)

    else:
        form = ProjectForm(instance=project)

    context = {
        'project': project,
        'form': form
    }
    return render(request, 'project/single.html', context)