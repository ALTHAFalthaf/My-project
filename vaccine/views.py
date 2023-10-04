from django.shortcuts import render, redirect
from .models import Usertable
from django.contrib.auth import authenticate, login as auth
from django.contrib import messages
from datetime import datetime
# Create your views here.
def index(request):
    return render(request, "index.html")

def homepage(request):
    return render(request, "homepage.html")

def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user= Usertable.objects.get(email=email, password=password) if Usertable.objects.filter(email=email).exists() else None

        if user is not None:
            auth(request, user)
            messages.success(request, "Login successfull")
            return redirect('homepage')
        else:
            messages.info(request, "invalid login")
            return redirect('login')
         
    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob_str = request.POST['dob']
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        role = request.POST['role']
        password = request.POST['password']
        

        # Validate the inputs
        if not fname or not lname or not email or not phone or not dob or not role or not password:
            messages.info(request, "All fields are required")
            return redirect('signup')
        elif Usertable.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('signup')
      
        user = Usertable( email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')
    
    return render(request, "signup.html")
