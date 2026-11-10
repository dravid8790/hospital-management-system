from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "phone", "consultation_fee", "is_active")
    list_filter = ("specialty", "is_active")
    search_fields = ("name", "specialty", "email")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "appointment_time", "status")
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("patient__username", "doctor__name")
    list_editable = ("status",)
