from django.db import models
from django.contrib.auth.models import User


#create models here

# course of a study session 
class Course(models.Model): 
    name = models.CharField(max_length=300); 

    def __str__(self):
        return self.name

#study session mdoel
class Study_Session(models.Model):
    # Unique attributes of a study session
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='study_sessions')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True)  # Add a name field
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Order based on creation
    class Meta: 
        ordering = ['-updated', 'created']
    
    def __str__(self): 
        return self.name

