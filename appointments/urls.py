from django.urls import path
from .views import ServiceListView, ServiceUpdateView, ServiceDeleteView, ServiceCreateView,\
    MasterListView, MasterUpdateView, MasterCreateView, MasterDeleteView, AppointmentCreateView, \
    AppointmentDetailView, AppointmentUpdateView, AppointmentListView, AppointmentDeleteView


urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('service/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
    path('service/new/', ServiceCreateView.as_view(), name="service_new"),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('masters/service/<int:service_id>/', MasterListView.as_view(), name='master_list'),
    path('masters/<int:pk>/edit/', MasterUpdateView.as_view(), name='master_edit'),
    path('masters/new/', MasterCreateView.as_view(), name='master_new'),
    path('masters/<int:pk>/delete/', MasterDeleteView.as_view(), name='master_delete'),
    path('appointment/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:master_pk>/<int:service_pk>/new/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointment/<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointment/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_confirm_delete'),
]
