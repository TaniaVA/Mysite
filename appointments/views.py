from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Service, Master, Appointment, Availability
from .forms import AppointmentForm

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AvailableDatesView(TemplateView):
    template_name = 'available_dates.html'

def available_dates(request):
    services = Service.objects.all()
    masters = Master.objects.all()
    context = {'services': services, 'masters': masters}
    if request.method == 'POST':
        selected_service = request.POST.get('service')
        selected_master = request.POST.get('master')
        service = Service.objects.get(pk=selected_service)
        master = Master.objects.get(pk=selected_master)
        available_dates = []
        for availability in Availability.objects.filter(service=service, master=master):
            available_dates.append(availability.date)
        context['available_dates'] = available_dates
        context['selected_service'] = service
        context['selected_master'] = master
    return render(request, 'available_dates.html', context)

class AvailableTimesView(TemplateView):
    template_name = 'available_times.html'

def available_times(request, service_id, master_id, year, month, day):
    service = Service.objects.get(pk=service_id)
    master = Master.objects.get(pk=master_id)
    selected_date = timezone.datetime(int(year), int(month), int(day)).date()
    available_times = Availability.objects.filter(service=service, master=master, date=selected_date)
    form = AppointmentForm()
    context = {'service': service, 'master': master, 'selected_date': selected_date, 'available_times': available_times, 'form': form}
    return render(request, 'available_times.html', context)

class CreatAppointmentView(FormView):
    template_name = 'create_appointment.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment_list')

def create_appointment(request, service_id, master_id, year, month, day, start_hour, start_minute):
    service = Service.objects.get(pk=service_id)
    master = Master.objects.get(pk=master_id)
    selected_date = timezone.datetime(int(year), int(month), int(day)).date()
    start_time = timezone.datetime(int(year), int(month), int(day), int(start_hour), int(start_minute)).time()
    end_time = (timezone.datetime.combine(selected_date, start_time) + service.duration).time()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = service
            appointment.master = master
            appointment.date = selected_date
            appointment.time = start_time
            appointment.save()
            return redirect(reverse_lazy('appointments:thank_you'))
    else:
        form = AppointmentForm()
    context = {'service': service, 'master': master, 'selected date': selected_date, 'start_time': start_time,
               'end_time': end_time, 'form': form}
    return render(request, 'create_appointment.html', context)

class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    template_name = "service_new.html"
    fields = ['name', 'price', 'duration',]

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    template_name = 'service_edit.html'
    fields = ['name', 'price', 'duration',]

class MasterListView(LoginRequiredMixin, ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'

class MasterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Master
    template_name = "master_new.html"
    fields = ['name',]

class MasterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('master_list')

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointment'

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(client=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

@login_required
def appointment_detail(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    return render(request, 'appointment_detail.html', {'appointment': appointment})


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_edit.html'


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment_list')
    template_name = 'appointment_confirm_delete.html'

class MakeAppointmentView(FormView):
    template_name = 'make_appointment.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment_list')

@login_required
def make_appointment(request, master_id):
    master = Master.objects.get(pk=master_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.master = master
            if master.is_available(appointment.date, appointment.time):
                appointment.save()
                messages.success(request, 'Appointment was successfully created.')
                return redirect('appointment_list')
            else:
                messages.error(request, 'This time slot is already taken. Please choose another one.')
    else:
        form = AppointmentForm()

    return render(request, 'make_appointment.html', {'form': form, 'master': master})

