import json

from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import AppointmentForm, MasterForm, ServiceForm
from .models import Appointment, Master, Service


# List view for Service model
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'


# Create view for Service model
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_create.html'


# Update view for Service model
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_update.html'


# Delete view for Service model
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')


# Detail view for Service model
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'


# List view for Master model
class MasterListView(ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'

    def get_queryset(self):
        # Get all masters that have the current service in their services list
        return Master.objects.filter(services__pk=self.kwargs['service_id']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current service object and add it to the context
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        return context


# Create view for Master model
class MasterCreateView(CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_create.html'
    success_url = reverse_lazy('master_list')


# Update view for Master model
class MasterUpdateView(UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_update.html'
    success_url = reverse_lazy('master_list')

    def get_object(self):
        # Get the current master object by its primary key
        return get_object_or_404(Master, pk=self.kwargs['pk'])

    def form_valid(self, form):
        master = form.save(commit=False)
        # Save the uploaded photo to the server and set it as the master's photo
        photo = form.cleaned_data['photo']
        if photo:
            file_name = default_storage.save(photo.name, ContentFile(photo.read()))
            master.photo = file_name
        master.save()
        return super().form_valid(form)


# Delete view for Master model
class MasterDeleteView(DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('master_list')


# Detail view for Master model
class MasterDetailView(DetailView):
    model = Master
    template_name = 'master_detail.html'
    context_object_name = 'master'

    # The get_context_data method adds the selected service and schedule_dict to the context of the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        master = self.get_object()
        schedule_dict = master.get_schedule_dict()
        context['schedule_dict'] = schedule_dict
        return context

    # The post method processes the form data submitted by the user.
    # If the form is valid, it creates a new Appointment instance and
    # redirects to the success URL. If the form is invalid, it adds an
    # error message to the context and renders the template again with the invalid form.
    def post(self, request, *args, **kwargs):
        master = self.get_object()
        service = get_object_or_404(Service, pk=self.kwargs['service_id'])
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = service
            appointment.master = master
            appointment.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('service_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
            return self.render_to_response(self.get_context_data(form=form))

# The following code defines a view to create a new Appointment instance
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('appointment_create_success')

    # The form_invalid method is called when the form is invalid.
    # t adds the selected time to the context and renders the template again with the invalid form.
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # добавляем время в контекст шаблона
        context['time'] = self.request.POST.get('time')
        return self.render_to_response(context)

    # The get_form_kwargs method adds the initial data for the master and service fields of the form.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'master': self.get_object(),
            'service': get_object_or_404(Service, pk=self.kwargs['service_id'])
        }
        return kwargs

    # The get_object method gets the Master object based on the pk URL parameter.
    def get_object(self):
        return get_object_or_404(Master, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Запись успешно создана!')
            return self.form_valid(form)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
            return self.form_invalid(form)

    # The form_valid method is called when the form is valid. It saves the form data to the database and
    # redirects to the success URL.
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    # The get_context_data method adds the selected service, schedule_dict,
    # and object  to the context of the template. It also adds the available
    # time options for the time form field based on the schedule of the selected
    # Master object. Finally, it returns the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        master = get_object_or_404(Master, pk=self.kwargs['pk'])
        schedule_dict = master.get_schedule_dict()
        context['schedule_dict'] = schedule_dict

        # let's add time options for the time form field
        available_times = []
        for schedule in schedule_dict.values():
            for time, status in schedule.items():
                if status == 'available':
                    available_times.append((time, time))
        context['form'].fields['time'].widget.choices = available_times
        context['schedule'] = schedule_dict
        context['object'] = self.object

        return context

# The AppointmentCreateSuccessView simply renders the success template
class AppointmentCreateSuccessView(TemplateView):
    template_name = 'appointment_create_success.html'

