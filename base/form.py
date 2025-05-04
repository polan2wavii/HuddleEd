from django.forms import ModelForm
from django.forms.widgets import TextInput  # Explicitly import TextInput
from .models import Study_Session, Course
from django.contrib.auth.models import User
from .models import Study_Session, Course
from django.contrib.auth.models import User
from django.forms.widgets import TextInput



class StudySessionForm(ModelForm):
    class Meta:
        model = Study_Session
        fields = '__all__'
        exclude = ['host']

class UserSearchForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Search for users...'}),
        }
        labels = {
            'username': 'Search Users',
        }