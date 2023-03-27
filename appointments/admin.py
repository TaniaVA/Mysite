from django.contrib import admin
from .models import Service, Master

from .models import Appointment
# Register your models here.
admin.site.register(Appointment)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    list_filter = ('name', 'duration', 'price')
    search_fields = ('name',)
    pass

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass