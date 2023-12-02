from django import forms
from .models import Schedule, Record, Vaccine, Immunogen

class ScheduleForm(forms.ModelForm):    
    exp_date = forms.CharField(label='Vaccine Expiration Date')
    date_immunized = forms.CharField(label='Date of Immunization',
                                     widget=forms.TextInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'dd/mm/yy',

                                     }))
    exp_date = forms.CharField(label='Vaccine Expiration Date',
                                     widget=forms.TextInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'dd/mm/yy',

                                     }))
    vaccine_type = forms.ModelChoiceField(queryset=Vaccine.objects.all(), initial=0, label="Vaccine Type")

    class Meta:
        model = Schedule
        fields = [ 'date_immunized','vaccine_type','exp_date']

TIME = (
    ('B', 'Birth'),
    ('6w', '6 weeks (Infants)'),
    ('10w', '10 weeks (Infants)'),
    ('14w', '14 weeks (Infants)'),
    ('6m', '6 moonths (Infants)'),
    ('9m', '9 months (Infants)'),
    ('12m', '12-24 months (Infants)'),
    ('15m', '15-18 months (Infants)'),
    ('24m', '24 months (Infants)'),
    ('L', 'Less than 13 years '),
)


class VaccineForm(forms.ModelForm):
    timing = forms.ChoiceField(label="Age/Timing", choices=TIME)
    imu_id = forms.ModelChoiceField(queryset=Immunogen.objects.all(), initial=0, label="Vaccine Type")
    description = forms.CharField(label='Vaccine Description')
     
    class Meta:
        model = Vaccine
        fields =['timing', 'imu_id', 'description']



