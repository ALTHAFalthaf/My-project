from django.contrib import admin
from django.urls import path
#from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
   path('',views.index,name='index'),
   path('signup', views.signup, name='signup'),
   path('login', views.loginn, name='login'),
   path('homepage', views.homepage, name='homepage'),
]
