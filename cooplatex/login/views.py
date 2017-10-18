from django.shortcuts import render
from .forms import RegisterForm, SignInForm
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login

# Create your views here.

# home page
def index(request):
    return render(request, 'login/index.html')

# signin Page
def signIn(request):
    if request.method == 'GET':
        form = SignInForm()
        return render(request, 'login/signin.html',
             {'form': form})
    else:
        return login(request)

# login submition handler
def login(request):
    form = SignInForm(request.POST)
    error_message = 'Unknown error occured. Please try later.'

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(request, username=email, password=password) 
        if user is not None:
            print("HELLLLLO")
            # TODO: user verified check here  <------------------------------------------>
            login(request, user)
        error_message='Invalid login!'

    return render(request, 'login/signin.html', 
        {'form': form, 'error_message':error_message})


#  register page
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'login/register.html',
             {'form': form, 'done': False})
    else:
        return registerPost(request)

# register submition handler
def registerPost(request):
    form = RegisterForm(request.POST)
    error_message = 'Check that the fields are valid'

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password1 = form.cleaned_data['password1']

        if not password1 == password:
            error_message = "Password does not match"
            return render(request, 'login/register.html',
                 {'form': form, 
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
        
        return makeUser(name, email, password, request)
          
    return render(request, 'login/register.html',
         {'form': form, 
        'error_message': error_message})

def makeUser(name, email, password, request):
    verify_token = get_random_string(length=32)
    user = CustomUser.objects.create_user(email, password)
    user.verify_token = verify_token
    user.name = name
    user.save()
    # sendEmail(user)
    return render(request, 'login/register.html', {'done':True})

def sendEmail(user):
    # TODO: SEND USER VERIFICATION EMAIL  -------------------------------------------------------->
    pass

