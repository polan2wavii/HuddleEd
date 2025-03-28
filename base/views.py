from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django. contrib.auth.forms import UserCreationForm
from django.db.models import Q 
from django.contrib import messages
from .models import Study_Session

# Create your views here.
def home(request):
    #render all study sessions 

    return render(request, 'home.html')

def session(request, pk):
    session = Study_Session.objects.get(id=pk)
    description = session.description
    course = session.course
    preferences = session.preferences

    context = {'session': session, 'desciprtion': description, 'course': course, 'prefrences': preferences}

    return render(request, 'base/session.html', context)

def profile(request):
    return render(request, 'profile.html')

def register(request):
    account = UserCreationForm()
    if request.method == 'POST': 
        account = UserCreationForm(request.POST)
    if account.is_valid(): 
        user = account.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
    else: 
        messages.error("An error has occured. Try again later")
    return render(request, 'base/register.html')

def loginPage(request): 
    page: 'login'
    user = authenticate(username=request.POST.get('username'), passowrd=request.POST.get('password')) 

    if user is not None and user.is_authenticated:
       login(request, user)
       return redirect('home')
    else: 
        messages.error("username or password does not exist")

    return render(request, 'base/login_page.html')

def logutUser(request):
    logout(request) 
    return redirect('base/login_page.html')

@login_required(login_url='/login')
def create_session(request):
   
    return 1

@login_required(login_url='/login')
def update_sessoin(): 
    return 1
@login_required(login_url='/login')
def delete_session(request): 
    return