from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.session, name="room"),
    path('profile/', views.profile, name='profile')
]