
# from datetime import datetime
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from .models import Usertable



# # Create your views here.
# def index(request):
#     return render(request, "index.html")

# def about(request):
#     return render(request, "about.html")

# def contact(request):
#     return render(request, "contact.html")

# def signup(request):
#     if request.method == 'POST':
#         role = request.POST['role']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password = request.POST['password']
#         hashed_password = make_password(password)
#         user = Usertable(role=role, fname=fname, lname=lname,phone=phone, email=email, password=hashed_password)
#         user.save()
#         return redirect('login')
#     return render(request, "signup.html")

# def login(request):
#     return render(request, "login.html")

# def signin(request):
#     return render(request, "signin.html")





from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, get_user_model
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from datetime import datetime

# from .helpers import send_forget_password_mail
# from .forms import PatientProfileForm

# Create your views here.
def index(request):
    return render(request,'index.html')

# @login_required
def homepage(request):
    if 'email' in request.session:
        response = render(request, 'homepage.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')

def loginn(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['email']=email
            return redirect('homepage')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

    # return render(request,'login.html')
def signup(request):
    if request.method == "POST":
        firstname=request.POST.get('fname') 
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dob')
        username=request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
      
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser(first_name=firstname,last_name=lastname,email=email,phone=phone,dob=dob,username=username,role='CHILD')  # Change role as needed
            user.set_password(password)
            user.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request,'signup.html')

def user_logout(request):
    try:
        del request.session['email']
    except:
        return redirect('login')
    return redirect('login')

def adminreg(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    user_profiles = User.objects.all()
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    
    # Render the HTML template
    return render(request, 'adminreg.html', context)



# def logout(request):
#     return render(request, 'login.html')
# def logout(request):
#      if request.user.is_authenticated:
#       auth_logout(request) # Use the logout function to log the user out
#      return redirect('login')  # Redirect to the confirmation page

# def ChangePassword(request, token):
#     context = {}

#     try:
#         profile_obj = CustomUser.objects.filter(forget_password_token=token).first()

#         if profile_obj is None:
#             messages.success(request, 'Invalid token.')
#             return redirect('/forget-password/')

#         if request.method == 'POST':
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('reconfirm_password')

#             if new_password != confirm_password:
#                 messages.success(request, 'Passwords do not match.')
#                 return redirect(f'/change-password/{token}/')

#             # Update the password for the user associated with profile_obj
#             profile_obj.set_password(new_password)
#             profile_obj.forget_password_token = None  # Remove the token
#             profile_obj.save()
#             return redirect('/login/')

#     except Exception as e:
#         print(e)
    
#     return render(request, 'change-password.html', context)


# import uuid
# def ForgetPassword(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')
            
#             user_obj = CustomUser.objects.filter(username=username).first()
            
#             if user_obj is None:
#                 messages.error(request, 'No user found with this username.')
#                 return redirect('/forget-password/')
            
#             token = str(uuid.uuid4())
#             user_obj.forget_password_token = token
#             user_obj.save()
#             send_forget_password_mail(user_obj.email, token)
#             messages.success(request, 'An email has been sent with instructions to reset your password.')
#             return redirect('/forget-password/')
    
#     except Exception as e:
#         print(e)
    
#     return render(request, 'forget-password.html')

# def patient_profile(request):
#     patient = request.user
    
#     if request.method == 'POST':
#         form = PatientProfileForm(request.POST, instance=patient)
#         if form.is_valid():
#             form.save()
#     else:
#         form = PatientProfileForm(instance=patient)

#     return render(request, 'patient_profile.html', {'patient': patient, 'form': form})