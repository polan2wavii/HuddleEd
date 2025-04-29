from django.forms import ModelForm
from .models import Study_Session, Course


class StudySessionForm(ModelForm):
    class Meta:
        model = Study_Session
        fields = '__all__'
        exclude = ['host']