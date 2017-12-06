"""login app views"""

from django.shortcuts import render, redirect
from .forms import RegisterForm, SignInForm
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from .forms import RegisterForm, SignInForm
from .models import CustomUser

def index(request):
    """GET homepage"""
    # Check if there is a session
    if request.user.is_authenticated:
        return redirect("/dash/")
    return render(request, 'login/index.html')

def sign_in(request):
    """GET AND POST sign_in handler"""
    if request.method == 'GET':
        form = SignInForm()
        return render(request, 'login/signin.html',{'form': form})
    else:
        return login_handler(request)

def login_handler(request):
    """login POST handler"""

    form = SignInForm(request.POST)
    error_message = 'Unknown error occured. Please try later.'

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password) 
        if user is not None:
            # TODO: user verified check here
            if user.verified:
                login(request, user)
                request.session["user"] = email
                return redirect("/dash/")
            return redirect('/home/pleaseverify/')
        error_message = 'Invalid login!'

    return render(request, 'login/signin.html', {'form': form, 'error_message':error_message})

def register(request):
    """GET AND POST register handler"""
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'login/register.html', {'form': form, 'done': False})
    else:
        return register_post(request)

def register_post(request):
    """register POST handler"""
    form = RegisterForm(request.POST)
    error_message = 'Check that the fields are valid'

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password1 = form.cleaned_data['password1']

        if not password1 == password:
            error_message = "Password does not match"
            return render(request, 'login/register.html', {'form': form,
                'error_message': error_message})

        if len(password) < 8:
            error_message = "Password must be at least 8 characters long"
            return render(request, 'login/register.html',
                 {'form': form, 
                'error_message': error_message})

        if CustomUser.objects.filter(email=email).exists():
            error_message = "Email already in use"
            return render(request, 'login/register.html',
                {'form': form, 
                'error_message': error_message})

        return make_user(name, email, password, request)

    return render(request, 'login/register.html',
         {'form': form, 
        'error_message': error_message})

def make_user(name, email, password, request):
    """Creates a new user"""
    verify_token = get_random_string(length=32)
    user = CustomUser.objects.create_user(email, password)
    user.verify_token = verify_token
    user.name = name
    user.save()
    # sendEmail(user)
    # TODO: don't hard code url
    send_mail(
        'CoopLaTeX: verification email',
        'Here is your verification link: http://localhost:8000/home/verify/{}/{}'.format(user.id, user.verify_token),
        'cooplatex@outlook.com',
        [email],
        
    )
    return redirect('/home/pleaseverify/')

def verifyUser(request, userID, verifyToken):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(id=userID)
        except CustomUser.DoesNotExist:
            return HttpResponseNotFound('<h1>404<h1>')

        if user.verify(verifyToken):
            return render(request, 'login/success.html')
    return HttpResponseNotFound('<h1>Invalid verification link<h1>')

def pleaseVerify(request):
    print('HELLO1')
    if request.method == 'GET':   
        print('HELLO')
        return render(request, 'login/pleaseverify.html')
    return HttpResponseNotFound()