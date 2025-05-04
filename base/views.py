from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django. contrib.auth.forms import UserCreationForm
from django.db.models import Q 
from django.contrib import messages
from .models import Study_Session, Course
from .form import StudySessionForm, UserSearchForm
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Message

# Create your views here.
@login_required(login_url='/login')
def home(request):
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''

    sessions = Study_Session.objects.all()
    sessions_count = sessions.count()
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')

    #reminder purposes 
    today = now().date()
    tomorrow = today + timedelta(days=1)
    upcoming = Study_Session.objects.filter(
        host=request.user,
        date__range=[today, tomorrow]
    ).order_by('date', 'time')

    context = {'sessions': sessions, 'search_query': search_query, 'sessions_count': sessions_count, 'upcoming': upcoming, 'messages': messages}
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
            study_session.host = request.user  # Set the host to the logged-in user
            study_session.course = Course.objects.first()  # Set a default course or get it dynamically
            study_session.save()
            messages.success(request, 'Study session created successfully.')
            return redirect('home')
        else: 
            messages.error(request, 'An error has occurred. Please try again.')
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

#search for users
def user_search_view(request):
    form = UserSearchForm(request.POST)
    if form.is_valid():
        selected_user = form.cleaned_data.get('user')
        if selected_user:
            users = User.objects.filter(username__icontains=selected_user.username)
        else:
            users = User.objects.all()
    else:
        users = User.objects.all()

    context = {'form': form, 'users': users}
    return render(request, 'find_partner.html', context)

#message another user
def message_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        # Handle sending the message to the user
        messages.success(request, 'Message sent successfully.')
        return redirect('home')
    return render(request, 'message_user.html', {'user': user})
