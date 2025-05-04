from django.contrib import admin
from .models import Study_Session, Course, Message
# Register your models here.


class StudySessionAdmin(admin.ModelAdmin):
    exclude = ('host',)  # Hide 'host' field in Admin form

    def save_model(self, request, obj, form, change):
        if not obj.host:
            obj.host = request.user
        obj.save()
        
admin.site.register(Study_Session)
admin.site.register(Course)
admin.site.register(Message)