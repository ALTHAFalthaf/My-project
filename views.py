
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
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist 
from .models import Appointment
from .models import Doctor

# from .helpers import send_forget_password_mail
# from .forms import PatientProfileForm

# Create your views here.
def index(request):
    return render(request,'index.html')

 #@login_required
@never_cache
def homepage(request):
    if 'email' in request.session:
        response = render(request, 'homepage.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')









def doctor_added(request):
    return render(request, 'doctor_added.html')  # Display the success page


def doctor_home(request):
    return render(request, 'doctor_home.html')  # Display the success page




def view_doctor(request):
    return render(request, 'view_doctor.html')  # Display the success page

def doctor_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'doctor_list.html', context)

def doctor_home(request):
     return render(request, 'doctor_home.html')





def myprofile(request):
    return render(request, 'myprofile.html')

def editprofile(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)

        # Update user data with form data
        user.first_name = request.POST.get("fname")
        user.last_name = request.POST.get("lname")
        user.phone = request.POST.get("phone")
        user.save()

        # Display a success message using Django's messages framework
        messages.success(request, "Profile updated successfully!")

        # Redirect to the My Profile page
        return redirect('myprofile')

    return render(request, 'editprofile.html')



def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Try to retrieve the user by email
            user = authenticate(request, email=email, password=password)
            
            
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        request.session['email'] = email
                        auth_login(request, user)
                        return redirect('adminreg')
                    else:
                        request.session['email'] = email
                        auth_login(request, user)
                        # Check if the user is a doctor
                        if user.role == 'Doctor':
                            return redirect('doctor_home')
                        else:
                            return redirect('homepage')
                else:
                    error_message = "Invalid credentials"
                    messages.error(request, error_message)
            else:
                error_message = "Your account is not active. Please contact the admin."
                messages.error(request, error_message)

        except ObjectDoesNotExist:
            # User with the given email does not exist
            error_message = "User with this email does not exist. Please sign up."
            messages.error(request, error_message)

    response = render(request, 'login.html')
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
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
      
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser(first_name=firstname,last_name=lastname,email=email,phone=phone,dob=dob,role='CHILD')  # Change role as needed
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



    



from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.template.loader import render_to_string
from django.conf import settings

def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.email}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.email}' is already deactivated.")
    return redirect('adminreg')

def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('adminreg')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Doctor
from .models import Appointment 

def send_registration_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        registration_link = request.build_absolute_uri(reverse('doctor_registration'))
        subject = 'Doctor Registration Link'
        message = render_to_string('registration_email.html', {'name': name, 'registration_link': registration_link})
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
        send_mail(subject, message, from_email, [email])
        messages.success(request, f'Registration email sent to {email}')
        return redirect('adminreg')


def adminreg(request):
    User = get_user_model()
    
    if request.method == 'POST':
        if 'send_email' in request.POST:
            doctor_email = request.POST.get('doctor_email')
            message = "Your message goes here."  # Customize the email message
            send_mail('Subject', message, 'kiddoguard12@gmail.com', [doctor_email])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if 'email' in request.session:
        email = request.session['email']
        try:
            user = User.objects.get(email=email)
            if user.role == 'Admin':
                user_profiles = User.objects.all()

                # Filter doctors based on the 'approved' field
                doctors = Doctor.objects.filter(approved=False)
                approved_doctors = Doctor.objects.filter(approved=True)
                appointments = Appointment.objects.all()

                context = {'user_profiles': user_profiles, 'doctors': doctors, 'approved_doctors': approved_doctors,'appointment': appointment}
                return render(request, 'adminreg.html', context)
            else:
                messages.error(request, "You don't have permission to access this page.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('login')

def doctor_registration(request):
    if request.method == 'POST':
        # Get data from the submitted form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        specialty = request.POST.get('specialty')
        license_number = request.POST.get('license_number')
        certification = request.POST.get('certification')
        resume = request.FILES.get('resume')
        license_copy = request.FILES.get('license_copy')
        photo = request.FILES['photo']

        # Try to create a new Doctor object and handle IntegrityError
        try:
            doctor = Doctor(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                specialty=specialty,
                license_number=license_number,
                certification=certification,
                resume=resume,
                license_copy=license_copy,
                photo=photo,
                approved=False  # Set approved status to False by default
            )
            doctor.save()

            messages.success(request, 'Doctor registration successful. Waiting for approval.')
            return redirect('adminreg')
        except IntegrityError as e:
            # Handle the IntegrityError
            if 'UNIQUE constraint' in str(e):
                messages.error(request, 'A doctor with this email already exists.')
            else:
                messages.error(request, 'An error occurred during registration.')

    return render(request, 'doctor_registration.html')

    
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Doctor

User = get_user_model()

def approve_doctor(request, doctor_id):
    if request.method == 'POST':
        # Retrieve the doctor from the database
        doctor = Doctor.objects.get(id=doctor_id)

        # Check if the phone number is unique
        try:
            user = User.objects.get(phone=doctor.phone)
            messages.error(request, 'Phone number already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (doctor) with the doctor's details
            user = User(
                first_name=doctor.first_name,
                last_name=doctor.last_name,
                email=doctor.email,
                phone=doctor.phone,
                role='Doctor',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Aqwer12@'
            user.set_password(password)
            user.save()
            
            # Update the 'approved' status for the doctor
            doctor.approved = True
            doctor.save()

            # Send an email with the generated password
            subject = 'Your Doctor Homepage Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [doctor.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Doctor approved and password set.')

    return redirect('adminreg')







import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password



from django.shortcuts import render, redirect
from .models import Appointment, Doctor
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

@login_required  # This decorator ensures the user is authenticated


def make_appointment(request, doctor_id):
    
    doctor = Doctor.objects.get(pk=doctor_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.doctor = doctor    # Use the previously retrieved doctor instance
            appointment.save()
            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
         form = AppointmentForm(initial={'user_first_name': request.user.first_name, 'user_phone': request.user.phone,'doctor': doctor})
         

    return render(request, 'make_appointment.html', {'form': form,'doctor': doctor})

def appointment_confirmation(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})


from django.contrib.auth.decorators import login_required
from .models import Doctor

@login_required
def doctor_appointments(request):
    try:
        # Attempt to get the associated Doctor model for the current user
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # If a Doctor model doesn't exist, you can create one
        doctor = Doctor(user=request.user)  # Associate the user with the Doctor model
        doctor.save()

    # Now you can work with the 'doctor' object
    # ...

    return render(request, 'doctor_appointments.html', {'doctor': doctor})












































#@login_required
#def approve_doctor(request, doctor_id):
#    doctor = Doctor.objects.get(id=doctor_id)
 #   doctor.user = CustomUser.objects.create(
 #       email=doctor.email,
 #       role='Doctor',
 #       is_active=False  # Inactive until approved
 #   )
 #   doctor.user.set_unusable_password()  # Set an unusable password
 #   doctor.user.save()
  #  doctor.approved = True
  #  doctor.save() 

    # Send a registration link to the doctor
   # current_site = get_current_site(request)
    #subject = 'Doctor Registration Link'
    #message = 'Your doctor registration has been approved. Please complete your registration by clicking the link below.'
    #from_email = 'kiddoguard12@gmail.com'  # Replace with your email
   # recipient_list = [doctor.email] 
    #html_message = render_to_string('registration_link_email.html', {
      #  'user': doctor.user,
      ##  'domain': current_site.domain,
      #  'uid': urlsafe_base64_encode(force_bytes(doctor.user.pk)),
      #  'token': default_token_generator.make_token(doctor.user),
   # })

   # send_mail(subject, message, from_email, recipient_list, html_message=html_message)

   # messages.success(request, "Doctor registration approved. Registration link sent to the doctor's email.")
   # return redirect('adminreg')

#from django.contrib.auth.tokens import default_token_generator
#from django.contrib.auth import get_user_model, login
#from django.contrib.auth.decorators import login_required
#from django.contrib.sites.shortcuts import get_current_site
#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from django.shortcuts import render, redirect
#from django.contrib import messages

# ... (other imports)

#def doctor_registration_complete(request, uidb64, token):
  #  User = get_user_model()
  #  try:
 #       uid = force_text(urlsafe_base64_decode(uidb64))
  #      user = User.objects.get(pk=uid)
  #  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
   #     user = None

  #  if user is not None and default_token_generator.check_token(user, token):
    #    user.is_active = True
    #    user.save()

        # Log in the user
     #   auth_login(request, user)
     #   messages.success(request, "Doctor registration is complete. You are now logged in.")
      #  return redirect('homepage')
    #else:
     #   messages.error(request, "Doctor registration link is invalid or has expired.")
     #   return redirect('login')








    



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