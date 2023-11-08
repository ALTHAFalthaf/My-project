from django import forms
from .models import Appointment  # Import the Appointment model

class AppointmentForm(forms.ModelForm):
    user_first_name = forms.CharField(max_length=100, required=False)
    user_phone = forms.CharField(max_length=15, required=False)
    

    class Meta:
        model = Appointment
        fields = ['user_first_name', 'user_phone','appointment_date', 'appointment_time', 'description', 'comments']
