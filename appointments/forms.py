from django import forms
from .models import Master, Appointment, Availability
from django.utils import timezone
from datetime import datetime


class AppointmentForm(forms.ModelForm):
    time = forms.TimeField()
    date = forms.DateField(widget=forms.Select(choices=[]))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'


    class Meta:
        model = Appointment
        fields = ['service', 'master', 'date', 'time']

    def clean_time(self):
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        if not date or not time:
            raise forms.ValidationError('Выберите дату и время')

        available_times = self.available_times_func(date)
        if time not in available_times:
            raise forms.ValidationError('Выбранное время не доступно для записи')

        # Check that the selected time is not in the past
        selected_datetime = timezone.make_aware(datetime.combine(date, time))
        if selected_datetime < timezone.now():
            raise forms.ValidationError('Выбранное время уже прошло')

        return time

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError('Нельзя выбрать дату из прошлого')
        return date

    def crispy_detail_field(self, field, *args, **kwargs):
        if field.name == 'date':
            kwargs['id'] = 'id_date'
        return super().crispy_detail_field(field, *args, **kwargs)

class MasterForm(forms.ModelForm):
    schedule = forms.FileField(label='Расписание на месяц', required=False)

    class Meta:
        model = Master
        fields = ['name', 'photo', 'description', 'services', 'schedule']




