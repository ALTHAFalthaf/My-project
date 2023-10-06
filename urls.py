from django.contrib import admin
from django.urls import path
#from django.contrib.auth import views as auth_views
from .import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
   path('',views.index,name='index'),
   path('signup', views.signup, name='signup'),
   path('login', views.loginn, name='login'),
   path('homepage', views.homepage, name='homepage'),
   path('logout', views.user_logout, name='logout'),
   path('adminreg',views.adminreg, name='adminreg'),




   path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]