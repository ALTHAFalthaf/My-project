
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



def company_home(request):
    return render(request, 'company_home.html')


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
                    elif user.role == 'Company':
                        # Company login
                        request.session['email'] = email
                        auth_login(request, user)
                        return redirect('company_home') 
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
from django.contrib.auth.decorators import user_passes_test
from .models import Doctor
from .models import Appointment 
from .models import Company

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
@user_passes_test(lambda u: u.role == 'Admin', login_url='login')
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
                birth_details = BirthDetails.objects.all()
                companies = Company.objects.all()

                context = {'user_profiles': user_profiles, 'doctors': doctors, 'approved_doctors': approved_doctors,'appointments': appointments,'providers': providers,'birth_details': birth_details,'companies':companies}
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


from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Company

def approve_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company.is_verified = True
    company.status = 'Approved'  # Assuming 'status' is the field representing the status
    company.save()
    messages.success(request, 'Company approved successfully.')
    return redirect('adminreg')  # Redirect to wherever you want







from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BirthDetails

@login_required
def upload_birth_details(request):
    if request.method == 'POST':
        # Get the form data
        place_of_birth = request.POST.get('place_of_birth')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        regno = request.POST.get('regno')
        rchid = request.POST.get('rchid')

        # Check if the user is authenticated and is a CustomUser instance
        if request.user.is_authenticated:
            user = request.user

            # Check if the user already has birth details
            existing_birth_details = BirthDetails.objects.filter(user=user)
            if existing_birth_details.exists():
                message = 'Birth details already exist for this user.'
                return JsonResponse({'success': False, 'message': message})
                return redirect('birth_details_list')  # Redirect to the birth details list page
            else:
                # Create new birth details
                birth_details = BirthDetails.objects.create(
                    user=user,
                    place_of_birth=place_of_birth,
                    weight=weight,
                    height=height,
                    regno=regno,
                    rchid=rchid
                )
                message = 'Birth details uploaded successfully.'
                birth_details_list_url = reverse('birth_details_list')  # Get URL of birth_details_list page
                return JsonResponse({'success': True, 'message': message, 'redirect_url': birth_details_list_url})
        else:
            messages.error(request, 'Authentication error: Please log in with a valid user account.')
            return redirect('login')  # Redirect to the login page if the user is not authenticated

    try:
        # Fetch additional user details for pre-filling the form
        user_details = request.user
        child_namea = user_details.first_name
        child_nameb = user_details.last_name
        date_of_birth = user_details.dob
        gender = user_details.gender

        # Pass user details to the template
        context = {
            'user': request.user,
            'child_namea': child_namea,
            'child_nameb': child_nameb,
            'date_of_birth': date_of_birth,
            'gender': gender
        }

    except CustomUser.DoesNotExist:
        messages.error(request, 'User details not found.')
        return redirect('birth_details_error')  # Redirect to an error page or any other page

    return render(request, 'upload_birth_details.html', context)





from django.shortcuts import render, get_object_or_404
from .models import BirthDetails, CustomUser

def view_birth_details(request, user_id):
    user_profile = get_object_or_404(CustomUser, id=user_id)
    birth_details = BirthDetails.objects.filter(user=user_profile)
    return render(request, 'birth_details.html', {'user_profile': user_profile, 'birth_details': birth_details})






    
    
from django.shortcuts import render

def birth_details_list(request):
     return render(request, 'birth_details_list.html')

import csv
from django.http import HttpResponse
from .models import BirthDetails

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="birth_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Child Name', 'Date of Birth', 'Gender', 'Place of Birth', 'Weight', 'Height', 'Registration No', 'RCH ID'])

    birth_details = BirthDetails.objects.all()
    for detail in birth_details:
         writer.writerow([detail.user.first_name, detail.user.dob, detail.user.gender, detail.place_of_birth, detail.weight, detail.height, detail.regno, detail.rchid])

    return response




# import pandas as pd
# import os
# from django.conf import settings
# from django.http import HttpResponse
# from .models import Vaccine



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vaccine
import pandas as pd
from django.contrib import messages
from django.conf import settings

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        # Check if the data has already been loaded
        if not settings.VACCINES_DATA_LOADED:
            try:
                # Read the Excel file into a pandas DataFrame
                excel_data = pd.read_excel(excel_file)
                
                # Iterate over DataFrame rows and create Vaccine instances
                for index, row in excel_data.iterrows():
                    vaccine = Vaccine(
                        name=row['Vaccine name'],
                        edition_date=row['Edition Date'],
                        edition_status=row['Edition Status'],
                        last_updated_date=row['Last Updated Date'],
                        price=row['price']  # Modify this according to your Excel column name
                    )
                    vaccine.save()

                # Set the flag to indicate that the data has been loaded
                settings.VACCINES_DATA_LOADED = True
               
                message = "Vaccines loaded successfully."
                return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'success'})
            except Exception as e:
                message = "An error occurred: " + str(e)
                return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'danger'})
        else:
            message = "Vaccines already loaded."
            return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'warning'})
    else:
        return render(request, 'upload_excel.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Vaccine, Company, CartItem


@login_required
def view_available_vaccines(request):
    user = request.user
    if user.is_admin:  # Assuming you have a field 'is_admin' in your CustomUser model
        # Admin can view all available vaccines
        vaccines = Vaccine.objects.all()
        return render(request, 'view_available_vaccines.html', {'vaccines': vaccines})
    elif user.company:
        # Users associated with a company can view available vaccines
        vaccines = Vaccine.objects.all()
        return render(request, 'view_available_vaccines.html', {'vaccines': vaccines})
    else:
        # Users not associated with any company are not authorized to view vaccines
        messages.error(request, 'You are not associated with a licensed company.')
        return redirect('home')  # Redirect to home page or any other appropriate page




def add_to_cart(request, vaccine_id):
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user
        # Create or update the cart item for the user and vaccine
        cart_item, created = CartItem.objects.get_or_create(user=user, vaccine=vaccine)
        cart_item.quantity += quantity
        cart_item.save()
        return redirect('view_cart')
    return render(request, 'add_to_cart.html', {'vaccine': vaccine})
 


def update_cart(request):
    if request.method == 'POST':
        vaccine_id = request.POST.get('vaccine_id')
        action = request.POST.get('action')

        # Retrieve the cart item from the database
        cart_item = get_object_or_404(CartItem, vaccine__id=vaccine_id, user=request.user)

        # Update the quantity based on the action
        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # If quantity is already 1, delete the cart item
                cart_item.delete()

        # Save the updated cart item
        cart_item.save()

    return redirect('view_cart')

def remove_from_cart(request):
    if request.method == 'POST':
        # Retrieve the vaccine ID from the form data
        vaccine_id = request.POST.get('vaccine_id')

        # Retrieve the corresponding cart item from the database
        cart_item = get_object_or_404(CartItem, vaccine_id=vaccine_id, user=request.user)

        # Remove the cart item from the cart
        cart_item.delete()

        messages.success(request, "Item removed from the cart successfully.")
        return redirect('view_cart')  # Redirect back to the cart page
    else:
        # If the request method is not POST, redirect to a suitable page
        return redirect('view_cart')  # Redirect to the cart page or another page as needed


def delete_vaccine(request, vaccine_id):
    # Retrieve the vaccine object
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    
    # Check if the requesting user is a company user
    if request.user.company:
        # Delete the vaccine
        vaccine.delete()
        messages.success(request, 'Vaccine deleted successfully.')
    else:
        # If the user is not a company user, display an error message
        messages.error(request, 'You are not authorized to delete vaccines.')
    
    # Redirect back to the view_available_vaccine page or any other appropriate page
    return redirect('view_available_vaccines')




def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = Decimal(0)  # Initialize total price as Decimal
    for cart_item in cart_items:
        total_price += cart_item.subtotal
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vaccine, Checkout, CartItem, CheckoutItem
from decimal import Decimal
import razorpay

@login_required
def checkout(request):
    if request.method == 'POST':
        # Retrieve the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Calculate total price
        total_price = sum(item.subtotal for item in cart_items)

        # Extract shipping information from the form
        full_name = request.POST.get('full_name')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')  # Optional field
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        phone_number = request.POST.get('phone_number')

        # Save checkout information
        checkout = Checkout.objects.create(
            user=request.user,
            full_name=full_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pin_code=pin_code,
            phone_number=phone_number
        )

        for item in cart_items:
            CheckoutItem.objects.create(
                checkout=checkout,
                vaccine=item.vaccine,
                quantity=item.quantity,
                subtotal=item.subtotal
            )

        # Clear the user's cart after checkout
        cart_items.delete()

        # Redirect to a thank you page or order summary page
        return redirect('order_confirm', checkout_id=checkout.id)  # Replace 'order_summary' with your actual view name
    else:
        # If the request method is GET, retrieve cart items and calculate total price
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.subtotal for item in cart_items)

        # Pass cart items and total price to the template
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, 'checkout.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Checkout, CheckoutItem

def order_confirm(request, checkout_id):
    try:
        # Retrieve the checkout information using the provided checkout_id
        checkout = get_object_or_404(Checkout, pk=checkout_id)

        # Retrieve checkout items associated with the checkout
        checkout_items = checkout.items.all()

        # Calculate total price from checkout items
        total_price = sum(item.subtotal for item in checkout_items)

        context = {
            'checkout': checkout,
            'checkout_items': checkout_items,
            'total_price': total_price,
        }
        return render(request, 'order_confirm.html', context)
    except Checkout.DoesNotExist:
        messages.error(request, "No checkout information found. Please complete the checkout process first.")
        return redirect('view_cart')  # Redirect to the cart page
        



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vaccine, Checkout, CartItem, CheckoutItem
from decimal import Decimal
import razorpay

@login_required
def process_payment(request):
    if request.method == 'POST':
        # Retrieve the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Calculate total price
        total_price = sum(item.subtotal for item in cart_items)

        # Initialize Razorpay client
        client = razorpay.Client(auth=("rzp_test_EZL2rQubxJwxrv", "RhRefR6hrzAdlzxNVUm6s4Ja")) 

        # Convert total price to paise
        amount_in_paise = int(total_price * 100)

        # Create payment order
        data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": "vaccine_order",
            "notes": {
                "description": "Payment for vaccine purchase"
            }
        }

        try:
            payment = client.order.create(data=data)

            # Render the checkout page with payment details
            return render(request, 'process_payment.html', {'amount': amount_in_paise, 'payment': payment})

        except Exception as e:
            # Handle payment processing errors
            messages.error(request, f"Payment processing error: {str(e)}")
            return redirect('view_cart')

    else:
        # If request method is not POST, redirect to the cart
        return redirect('view_cart')



    







def purchase_success(request):
    return render(request, 'purchase_success.html')



# views.py
from django.shortcuts import render, redirect
from .models import Company

def register_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        license_number = request.POST.get('license_number')
        address = request.POST.get('address')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        Company.objects.create(
            name=name,
            license_number=license_number,
            address=address,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        return redirect('adminreg')
    return render(request, 'register_company.html')

# def company_list(request):
#     companies = Company.objects.all()
#     return render(request, 'company_list.html', {'companies': companies})


from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Company  # Import the Company model

User = get_user_model()

def generate_password_company(request, company_id):
    if request.method == 'POST':
        # Retrieve the company from the database
        company = Company.objects.get(id=company_id)

        # Check if the email is unique
        try:
            user = User.objects.get(email=company.contact_email)
            messages.error(request, 'Email already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (company) with the company's details
            user = User(
                first_name=company.name,  # Use company name as first name
                email=company.contact_email,
                phone=company.contact_phone,
                role='Company',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Qwer123@'
            user.set_password(password)
            user.save()

            # Send an email with the generated password
            subject = 'Your Company Account Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [company.contact_email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Company approved and password set.')

    return redirect('adminreg')



# def upload_excel(request):
#     return render(request, 'upload_excel.html')








































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