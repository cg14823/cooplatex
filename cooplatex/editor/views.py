"""Editor app views"""
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from .forms import ProjectCreateForm
from .models import Project
import json
import re

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

    return render(request, 'editor/index.html', context)


@login_required(login_url='/home/signin/')
def sign_out(request):
    """Sign out user"""
    logout(request)
    return redirect('/home')

@login_required(login_url='/home/signin/')
def create_porject(request):
    """ creates a project """

    failed = {
        "error_message":"Invalid request",
        "statusCode":400,
    }

    if request.method =='POST':
        project_name = request.POST.get("name")
        if (not re.match(r'^[a-zA-Z][0-9a-zA-Z_]+$', project_name) and len(project_name) < 3 
            and len(project_name) > 25):
            failed["error_message"] = "Invalid project name."
            return HttpResponse(json.dumps(failed), content_type="application/json")
    
        if Project.objects.filter(owner=request.user, name=project_name).exists():
            failed["error_message"] = "Project with this name already exists"
            return HttpResponse(json.dumps(failed), content_type="application/json")
        
        try:
            request.user.create_project(project_name)
        except ValueError:
            failed["error_message"] = "Could not create project at the moment try later."
            failed["status_code"] = 500
            return HttpResponse(json.dumps(failed), content_type="application/json")
        
        url = "/{}/{}".format(request.user.id, project_name)
        return HttpResponse( 
            json.dumps({"statusCode":200, "url":url}), 
            content_type="application/json"
        )

    return HttpResponse(json.dumps(failed), content_type="application/json")
    
