from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from datetime import datetime
from .models import CustomUser


# Create your views here.
def index(request):
    return render(request, "index.html")

def homepage(request):
    if 'email' in request.session:
        response = render(request,'homepage.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')

def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email, password=password)
            auth(request, user)
            request.session['email'] = email
            messages.success(request, "Logged in")
            return redirect('homepage')
        except CustomUser.DoesNotExist:
            messages.info(request, "Invalid login")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob_str = request.POST['dob']
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        role = request.POST['role']
        password = request.POST['password']
        

        # Validate the inputs
        if not first_name or not last_name or not email or not phone or not dob or not role or not password:
            messages.info(request, "All fields are required")
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('signup')
        username = email
        user = CustomUser( first_name=first_name, last_name=last_name,email=email,phone=phone,dob=dob, role=role, password=password, username=username)
        user.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')
    
    return render(request, "signup.html")



def logout(request):
    auth_logout(request)
    return render(request, 'login.html')

