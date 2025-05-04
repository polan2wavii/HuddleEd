from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.session, name="room"),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('create_session', views.create_session, name='create_session'),
    path('delete_session/<str:pk>', views.delete_session, name='delete_session'),
    path('update_session/<str:pk>', views.update_session, name="update_session"),
    path('find_partner/', views.user_search_view, name='find_partner'),
    #path('find_group/', views.find_group, name='find_group'),
]