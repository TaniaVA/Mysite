from django.urls import path
from .views import AvailableDatesView, AvailableTimesView, CreatAppointmentView, ServiceListView, ServiceCreateView,\
    ServiceDeleteView, ServiceUpdateView, MasterListView, MasterCreateView, MasterDeleteView, AppointmentCreateView, \
    AppointmentUpdateView, AppointmentListView, AppointmentDeleteView, AppointmentDetailView, MakeAppointmentView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path("service/new/", ServiceCreateView.as_view(), name="service_new"),
    path('service/<int:pk>/edit/', ServiceUpdateView.as_view(), name="service_edit"),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('availability/', AvailableDatesView.as_view(), name="available_dates"),
    path('availability/', AvailableTimesView.as_view(), name="available_times"),
    path('masters/', MasterListView.as_view(), name='master_list'),
    path('masters/', MasterCreateView.as_view(), name='master_new'),
    path('masters/', MasterDeleteView.as_view(), name='master_delete'),
    path('appointment/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/', CreatAppointmentView.as_view(), name='create_appointment'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/create/', AppointmentCreateView.as_view(), name='appointment_form'),
    path('appointment/<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_confirm_delete'),
    path('appointment/', MakeAppointmentView.as_view(), name='make_appointment'),
]



