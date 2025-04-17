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
    page = 'login'
    if request.method == "POST": 
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #authenticate user
        try: 
            user = User.objects.get(username=username)
        except: 
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    
    context = {'login': page}
    return render(request, 'home.html', context)

def session(request, pk):
    session = Study_Session.objects.get(id=pk)
    description = session.description
    course = session.course
    preferences = session.preferences

    context = {'session': session, 'desciprtion': description, 'course': course, 'prefrences': preferences}
    return render(request, 'base/session.html', context)

def profile(request, pk):
    user = User.objects.get(id=pk)
    sessions = user.studysession_set.all()
    context = {'user': user, 'sessions': sessions}
    return render(request, 'profile.html', context)

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
   form = Study_SessionForm()
   if request.method == 'POST': 
       form = Study_SessionForm(request.POST)
       if form.is_valid(): 
           study_session = form.save(commit=False)
           study_session.user = request.user
           study_session.save()
           return redirect('home')
       else: 
           messages.error(request, 'An error has occured. Try again later')
           return redirect('home')

@login_required(login_url='/login')
def update_sessoin(): 
    return 1

@login_required(login_url='/login')
def delete_session(request): 
    return