"""Editor app views"""
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from .forms import ProjectCreateForm
from .models import Project

@login_required(login_url='/home/signin/')
def index(request):
    """GET dashboard"""
    # TODO: load available files
    projects = request.user.get_my_projects()
    shared_projects = request.user.get_shared_with_me()
    has_project = projects.count() > 0 or shared_projects.count() > 0

    context = {
        'form': ProjectCreateForm(),
        'has_project': has_project,
        'my_projects': projects,
        'shared_projects': shared_projects,
    }

    if request.method == "GET":
        return render(request, 'editor/index.html', context)
    elif request.method == "POST":
        return create_porject(request, context)

@login_required(login_url='/home/signin/')
def sign_out(request):
    """Sign out user"""
    logout(request)
    return redirect('/home')


def create_porject(request, context):
    """ creates a project """
    form = ProjectCreateForm(request.POST)

    if not form.is_valid():
        context["error_message"] = "Project name is invalid"
        return render(request, 'editor/index.html', context)
    
    project_name = form.cleaned_data['project_name']

    if Project.objects.filter(owner=request.user, name=project_name).exists():
        context["error_message"] = "You already have a project with that name!"
        return render(request, 'editor/index.html', context)

    try:
        request.user.create_project(project_name)
    except ValueError:
        context["error_message"] = "Project name is invalid"
        return render(request, 'editor/index.html', context)

    # Should go to editor view
    context["success_message"] = "Project created"
    return render(request, 'editor/index.html', context)

    context["error_message"] = "Unknown error ocurred, please try later."
    return render(request, 'editor/index.html', context)
