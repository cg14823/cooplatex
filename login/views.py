from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.

# home page
def index(request):
    return render(request, 'login/index.html')

# signin Page
def signIn(request):
    return render(request, 'login/signin.html')

#  register page
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'login/register.html', {'form': form})
    else:
        return registerPost(request)

# register submition handler
def registerPost(request):
    form = RegisterForm(request.POST)
    error_message = 'Check that the fields are valid'

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password1 = form.cleaned_data['password1']

        if not password1 == password:
            error_message = "Password does not match"
            return render(request, 'login/register.html', {'form': form, 
                'error_message': error_message})

        if len(password) < 8:
            error_message = "Password must be at least 8 characters long"
            return render(request, 'login/register.html', {'form': form, 
                'error_message': error_message})
          
    return render(request, 'login/register.html', {'form': form, 
        'error_message': error_message})
