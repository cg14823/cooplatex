"""Editor app views"""
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponse
from .forms import ProjectCreateForm
from .models import Project
from .s3store import create_empty_file, get_files, save_file, get_pdf
from .compiler import compile_1_tex_file
from .s3store import create_empty_file
import json

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
        return create_project(request, context)

@login_required(login_url='/home/signin/')
def sign_out(request):
    """Sign out user"""
    logout(request)
    return redirect('/home')

def create_project(request, context):
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
    try:
        project = Project.objects.get(owner=request.user, name=project_name)
        # Create file here
        resp = create_empty_file(project.main_file, project_name, request.user.name)
    except Exception as e:
        print(e)
        context["error_message"] = "Project creation failed"
        return render(request, 'editor/index.html', context)

    # Should go to editor view
    context["success_message"] = "Project created"
    return HttpResponseRedirect('/dash')

@login_required(login_url='/home/signin/')
def editor_page(request, ownerID, projectName):
    if request.method == 'GET':
        try:
            if request.user.is_authenticated:
                # look up dajngo reques.user and how to authenticate
                #p = Project.objects.get(name=projectName)
                main_tex_body = get_files(projectName, ownerID)
        except Exception as e:
            print(e)
            return HttpResponseForbidden
        context = {
            'owner': ownerID,
            'projectName': projectName,
            'mainBody': main_tex_body, 
        }
        return render(request, 'editor/editorpage.html', context)

def save_project(request, ownerID, projectName):
    if request.method == 'POST':
        data = request.POST.get('file')
        if request.user.is_authenticated and data != None:
            print(request)
            filename = "{}-{}-main.tex".format(ownerID, projectName)
            response = save_file(filename, data)
            print(response)
            if response != None:
                json_return_ok = {"ok": "save successful"}
                return HttpResponse(status=200, content=json.dumps(json_return_ok), content_type='application/json')   
    
    error = {"error": "did not save successfully"}
    return HttpResponse(status=400, content=json.dumps(error), content_type='application/json')

def compile_project(request, ownerID, projectName):
    if request.method == 'POST':
        if request.user.is_authenticated:
            success, fileKey = compile_1_tex_file(ownerID, projectName)

            if not success:
                error = {"error": "did not compile successfully"}
                return HttpResponse(status=400, content=json.dumps(error), content_type='application/json')
            

            url = get_pdf(fileKey)
            if url != None:
                json_return_ok = {}
                json_return_ok["link"] = url
                json_return_ok["error_message"] = "Unable to display content"
                json_return_ok["status"] = 200
                return HttpResponse(status=200, content=json.dumps(json_return_ok), content_type='application/json')

    error = {"error": "did not compile successfully"}
    return HttpResponse(status=400, content=json.dumps(error), content_type='application/json')

def delete_project(request, ownerID, projectName):
    """delete project"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                p = Project.objects.get(owner= request.user.id, name=projectName)
                p.delete()
                deletedproject = "{}-{}".format(ownerID, projectName)
                responseDict = {"projectDeleted":deletedproject}
                return HttpResponse(status=200, content=json.dumps(responseDict), content_type='application/json')
            except Project.DoesNotExist:
                return HttpResponseNotFound()

        return HttpResponseForbidden()

    return HttpResponseBadRequest()

