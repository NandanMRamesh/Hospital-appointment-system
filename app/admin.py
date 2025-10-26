from django.contrib import admin
from .models import PatientProfile, DoctorProfile, Appointment


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'phone', 'date_of_birth')


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'specialization', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ('date', 'time', 'doctor', 'patient', 'status')
	list_filter = ('status', 'date', 'doctor')
	search_fields = ('patient__user__username', 'doctor__user__username')
