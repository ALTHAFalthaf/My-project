
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
from .models import HealthcareProvider


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


def about(request):
    return render(request, 'about.html')  


def contact(request):
    return render(request, 'contact.html')  





def doctor_added(request):
    return render(request, 'doctor_added.html')  # Display the success page





def view_doctor(request):
    return render(request, 'view_doctor.html')  # Display the success page


def doctor_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'doctor_list.html', context)





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
                error_message = "Incorrect username or Password"
                messages.error(request, error_message)

        except ObjectDoesNotExist:
            # User with the given email does not exist
            error_message = "User with this email does not exist. Please sign up."
            messages.error(request, error_message)

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
    # return render(request,'login.html')

@login_required
def signup(request):
    if request.method == "POST":
        firstname=request.POST.get('fname') 
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
      
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser(first_name=firstname,last_name=lastname,email=email,phone=phone,dob=dob,gender=gender,role='CHILD')  # Change role as needed
            user.set_password(password)
            user.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request,'signup.html')

@login_required
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
from django.contrib.auth.decorators import login_required
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

@login_required
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
                providers = HealthcareProvider.objects.all()

                context = {'user_profiles': user_profiles, 'doctors': doctors, 'approved_doctors': approved_doctors,'appointments': appointments,'providers': providers}
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
from django.contrib import messages
from .models import Appointment, Doctor
from django.contrib.auth.decorators import login_required

@login_required
def book_appointment(request, doctor_id):
    try:
        # Assuming that the doctor_id is passed in the URL
        doctor = Doctor.objects.get(id=doctor_id)

        if request.method == 'POST':
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            description = request.POST.get('description')
            comments = request.POST.get('comments')

            # Assuming the user is the patient making the appointment
            user = request.user

            # Create an Appointment object
            appointment = Appointment.objects.create(
                user=user,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                description=description,
                comments=comments
            )

            # Add any additional logic here (e.g., send confirmation email)

            
            return redirect('appointment_confirmation', appointment_id=appointment.id)  # You can redirect to a success page or any other page

        return render(request, 'book_appointment.html', {'doctor': doctor, 'user': request.user})

    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('appointment-error')  # You can redirect to an error page or any other page


from django.shortcuts import render
from .models import Appointment
import razorpay
from django.views.decorators.csrf import csrf_exempt

@login_required
def appointment_confirmation(request, appointment_id):
    amount_in_paise = int(500 * 100)
    
    DATA = {
        "amount": amount_in_paise,
        "currency":"INR",
        "receipt":"receipt1",
        "notes":{
            "key1": "value3",
            "key2": "value2",
        }
    }

    client = razorpay.Client(auth=("rzp_test_EZL2rQubxJwxrv","RhRefR6hrzAdlzxNVUm6s4Ja"))
    payment = client.order.create(data=DATA)

     # Assuming you have a variable indicating payment success
    payment_success = True  # Adjust this based on your payment logic

    context = {
        'amount': amount_in_paise,
        'payment': payment,
        
        
        
    }

    try:
        # Assuming the appointment_id is passed in the URL
        appointment = Appointment.objects.get(id=appointment_id)
        context['appointment'] = appointment
        return render(request, 'appointment_confirmation.html', context)

    except Appointment.DoesNotExist:
        # Handle the case where the appointment does not exist
        return render(request, 'appointment-error.html')




# views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Appointment

@require_POST
def check_time_availability(request):
    appointment_time = request.POST.get('appointment_time')
    appointment_date = request.POST.get('appointment_date')

    # Check if there is an existing appointment for the chosen time slot
    existing_appointment = Appointment.objects.filter(
        appointment_date=appointment_date,
        appointment_time=appointment_time
    ).exists()

    return JsonResponse({'available': not existing_appointment})




# views.py

from django.shortcuts import render
from .models import Doctor
from .models import Appointment
from django.contrib.auth.decorators import login_required

@login_required
def doctor_home(request):
    return render (request,'doctor_home.html')


@login_required
def doctor_appointments(request):
    doctor = request.user.doctor  # Assuming the doctor is associated with the user
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor_appointments.html', {'doctor': doctor, 'appointments': appointments})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

@login_required
def doctor_profile(request):
    doctor = request.user.doctor
    profile_updated = False  # Initialize the variable

    if request.method == 'POST':
        # Handle profile update
        doctor.first_name = request.POST.get('first_name', '')
        doctor.last_name = request.POST.get('last_name', '')
        doctor.email = request.POST.get('email', '')
        doctor.phone = request.POST.get('phone', '')

        # Handle photo upload
        photo = request.FILES.get('photo')
        if photo:
            # If a new photo is provided, save it and update the doctor's photo field
            photo_name = default_storage.save(f'doctor/photos/{user.doctor.id}/{photo.name}', photo)
            doctor.photo = photo_name
        doctor.save()

        # Fetch the updated data from the database
        doctor = Doctor.objects.get(id=doctor.id)

        profile_updated = True

    return render(request, 'doctor_profile.html', {'doctor': doctor, 'profile_updated': profile_updated})



@login_required
def change_password(request):
    password_updated = False  # Initialize the variable

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            password_updated = True
            update_session_auth_hash(request, user)  # Important to maintain the session
            

        else:
            messages.error(request, 'Error changing password. Please correct the errors.')
    else:
        form = PasswordChangeForm(request.user)


    return render(request, 'change_password.html', {'form': form,  'password_updated': password_updated})



 










#Vaccintion views


def vaccination_home(request):
    return render(request, 'vaccination_home.html')  









#payment

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_success(request):

    messages.success(request,'payment successfull')
    return redirect('homepage')




from django.shortcuts import render
from .models import Appointment

def appointment_history(request):
    # Retrieve all appointments and sort them by date
    appointments = Appointment.objects.all().order_by('appointment_date')

    # Pass the sorted appointments to the template
    return render(request, 'appointment_history.html', {'appointments': appointments})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HealthcareProvider

def signup_healthcare_provider(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        certification = request.POST.get('certification')
        resume = request.FILES.get('resume')
        license_copy = request.FILES.get('license_copy')
        photo = request.FILES.get('photo')

        try:
            # Create and save the HealthcareProvider instance
            provider = HealthcareProvider.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,  # Assuming 'phone' is the field name in the model
                license_number=license_number,
                certification=certification,
                resume=resume,
                license_copy=license_copy,
                photo=photo
            )
            messages.success(request, 'Healthcare provider added successfully.')
            return redirect('adminreg')  # Redirect to success page
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'signup_healthcare_provider.html')  # Replace 'your_template.html' with your actual template name



# views.py

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import HealthcareProvider

User = get_user_model()

def generate_password_provider(request, provider_id):
    if request.method == 'POST':
        # Retrieve the healthcare provider from the database
        provider = HealthcareProvider.objects.get(id=provider_id)

        # Check if the email is unique
        try:
            user = User.objects.get(email=provider.email)
            messages.error(request, 'Email already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (healthcare provider) with the provider's details
            user = User(
                first_name=provider.first_name,
                last_name=provider.last_name,
                email=provider.email,
                phone=provider.phone,
                role='Healthcare Provider',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Qwer123@'
            user.set_password(password)
            user.save()
            
            # Update the 'is_verified' status for the healthcare provider
            provider.is_verified = True
            provider.save()

            # Send an email with the generated password
            subject = 'Your Healthcare Provider Account Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [provider.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Healthcare provider approved and password set.')

    return redirect('adminreg')


from django.shortcuts import render, redirect
from .models import BirthDetails
from .models import CustomUser

def upload_birth_details(request):
    if request.method == 'POST':
        place_of_birth = request.POST.get('place_of_birth')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        regno = request.POST.get('regno')
        rchid = request.POST.get('rchid')

        # Assuming the user is the patient uploading the details
        user = request.user

        birth_details = BirthDetails.objects.create(
            user=user,
            place_of_birth=place_of_birth,
            weight=weight,
            height=height,
            regno=regno,
            rchid=rchid
        )
        return redirect('vaccination_home')  # Redirect to a success page after saving the details

    # Fetch additional user details for pre-filling the form
    user_details = CustomUser.objects.get(id=request.user.id)
    child_name = user_details.first_name
    date_of_birth = user_details.dob
    gender = user_details.gender

    # Pass user details to the template
    context = {
        'user': request.user,
        'child_name': child_name,
        'date_of_birth': date_of_birth,
        'gender': gender
    }

    return render(request, 'upload_birth_details.html', context)
















    





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