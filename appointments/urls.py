from django.urls import path
from .views import (AppointmentCreateView, MasterListView, MasterDetailView, MasterCreateView, MasterUpdateView,
                    MasterDeleteView, ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView, ServiceDetailView,
                    AppointmentCreateSuccessView)

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:service_id>/masters/', MasterListView.as_view(), name='master_list'),
    path('services/<int:service_id>/masters/create/', MasterCreateView.as_view(), name='master_create'),
    path('services/<int:service_id>/masters/<int:pk>/update/', MasterUpdateView.as_view(), name='master_update'),
    path('services/<int:service_id>/masters/<int:pk>/delete/', MasterDeleteView.as_view(), name='master_delete'),
    path('services/<int:service_id>/masters/<int:pk>/', MasterDetailView.as_view(), name='master_detail'),
    path('services/<int:service_id>/masters/<int:pk>/appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/success/', AppointmentCreateSuccessView.as_view(), name='appointment_create_success'),
]
