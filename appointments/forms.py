from django import forms
from .models import Master, Appointment, Service
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'master', 'date', 'time']
        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput(),
        }

class MasterForm(forms.ModelForm):
    pass

    class Meta:
        model = Master
        fields = ['name', 'photo', 'description', 'services', 'availability']

class ServiceForm(forms.ModelForm):
    pass

    class Meta:
        model = Service
        fields = ['name', 'price', 'duration', ]


