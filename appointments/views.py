from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Service, Master, Appointment, Availability
from .forms import AppointmentForm, MasterForm
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms
import datetime

class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    template_name = 'service_edit.html'
    fields = ['name', 'price', 'duration', ]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    template_name = "service_new.html"
    fields = ['name', 'price', 'duration', ]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')

class MasterListView(ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'
    success_url = reverse_lazy('appointment_create')

class MasterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Master
    template_name = 'master_edit.html'
    form_class = MasterForm
    success_url = reverse_lazy('master_list')

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

    def form_valid(self, form):
        # Получаем объект мастера из базы данных
        master = form.save(commit=False)
        # Получаем загруженное изображение из формы
        photo = form.cleaned_data['photo']
        # Если загружено изображение, то сохраняем его в файловой системе
        if photo:
            file_name = default_storage.save(photo.name, ContentFile(photo.read()))
            master.photo = file_name
        # Сохраняем изменения в базе данных
        master.save()
        return super().form_valid(form)


class MasterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Master
    template_name = "master_new.html"
    fields = ['name', 'description', 'availability', ]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff


class MasterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('master_list')

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointment_detail.html"

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('appointment_detail')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Проверяем, передан ли GET-параметр 'master_id'
        if 'master_id' in self.request.GET:
            # Получаем мастера из базы данных
            master = get_object_or_404(Master, id=self.request.GET['master_id'])
            # Получаем список доступных временных слотов для этого мастера
            availability_list = Availability.objects.filter(master=master, date__gte=datetime.date.today()).order_by(
                'date', 'start_time')
            # Создаем список временных слотов, который будет отображаться в выпадающем списке
            time_choices = []
            for availability in availability_list:
                time_choices.append((availability.id,
                                     f'{availability.date} {availability.start_time.strftime("%H:%M")} - {availability.end_time.strftime("%H:%M")}'))
            # Добавляем поле для выбора времени в форму
            form.fields['time'].widget = forms.RadioSelect(choices=time_choices)
        return form

    def form_valid(self, form):
        # Получаем выбранный временной слот
        availability = get_object_or_404(Availability, id=form.cleaned_data['time'])
        # Создаем объект записи
        appointment = form.save(commit=False)
        appointment.master = availability.master
        appointment.date = availability.date
        appointment.time = availability.start_time
        appointment.save()
        return super().form_valid(form)

class AppointmentListView(ListView):
    model = Appointment

    @login_required
    def appointment_list(request):
        appointments = Appointment.objects.filter(user=request.user)
        return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ['service', 'master', 'date', 'time']
    success_url = reverse_lazy('appointment_list')


class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment_list')

    @login_required
    def appointment_delete(request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
        if request.method == 'POST':
            appointment.delete()
            messages.success(request, 'Appointment has been deleted.')
            return redirect('appointment_list')
        return render(request, 'appointments/appointment_delete.html', {'appointment': appointment})
