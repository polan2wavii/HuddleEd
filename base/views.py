from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django. contrib.auth.forms import UserCreationForm
from django.db.models import Q 
from django.contrib import messages
from .models import Study_Session
from .form import StudySessionForm

# Create your views here.
@login_required(login_url='/login')
def home(request):
    #render all study sessions 
    page = 'login'
    sessions = Study_Session.objects.all()
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''     
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
    
    context = {'login': page, 'sessions': sessions, 'search_query': search_query}
    return render(request, 'home.html', context)

def session(request, pk):
    session = Study_Session.objects.get(id=pk)
    description = session.description
    course = session.course
    preferences = session.preferences

    context = {'session': session, 'desciprtion': description, 'course': course, 'prefrences': preferences}
    return render(request, 'session.html', context)

@login_required(login_url='/login')
def profile(request):
    user = request.user
    sessions = Study_Session.objects.filter(host=user)  # Filter sessions by the logged-in user
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
            print("avvount created")
            messages.success(request, "Account created successfully")
            return redirect('home')
        else: 
            messages.error(request, "An error has occurred. Try again later")
    return render(request, 'register.html', {'account': account})

def loginPage(request): 
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, "Username or password does not exist")

    return render(request, 'login_page.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def create_session(request):
   form = StudySessionForm()
   if request.method == 'POST': 
       form = StudySessionForm(request.POST)
       if form.is_valid(): 
           study_session = form.save(commit=False)
           study_session.host = request.user
           study_session.save()
           return redirect('home')
       else: 
           messages.error(request, 'An error has occured. Try again later')
           return redirect('home')
   return render(request, 'create_session.html', {'form': form})

@login_required(login_url='/login')
def update_session(): 
    return 1

@login_required(login_url='/login')
def delete_session(request, pk): 
    session = Study_Session.objects.get(id=pk)

    if request.method == 'POST': 
        session.delete()
        messages.success(request, 'Study session deleted successfully.')
        return redirect('home')
    
    return render(request, 'delete_session.html', {'obj': session})