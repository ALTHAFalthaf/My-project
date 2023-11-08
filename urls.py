from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
   path('myprofile',views.myprofile, name='myprofile'),
   path('editprofile',views.editprofile, name='editprofile'),
   path('send_registration_email/', views.send_registration_email, name='send_registration_email'),
   path('doctor_added/', views.doctor_added, name='doctor_added'),
   path('view_doctor/', views.view_doctor, name='view_doctor'),
   path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
   path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
   path('doctor_list/', views.doctor_list, name='doctor_list'),
   path('doctor_registration/', views.doctor_registration, name='doctor_registration'),
   path('approve_doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
   path('doctor_home/', views.doctor_home, name='doctor_home'),
   path('make_appointment/<int:doctor_id>/', views.make_appointment, name='make_appointment'),
   path('appointment_confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
   path('doctor_home/', views.doctor_home, name='doctor_home'),



#forgot_password code
   path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)