from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'service', 'doctor', 'date', 'time_slot', 'payment_method', 'payment_status')
    list_filter = ('payment_method', 'payment_status', 'date', 'doctor')
    search_fields = ('patient_name', 'email', 'phone')
