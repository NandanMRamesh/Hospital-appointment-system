from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
	phone = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)

	def __str__(self) -> str:
		return f"Patient: {self.user.get_full_name() or self.user.username}"


class DoctorProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
	specialization = models.CharField(max_length=100, blank=True)
	phone = models.CharField(max_length=20, blank=True)

	def __str__(self) -> str:
		return f"Dr. {self.user.get_full_name() or self.user.username} ({self.specialization})"


class Appointment(models.Model):
	STATUS_CHOICES = [
		('scheduled', 'Scheduled'),
		('completed', 'Completed'),
		('cancelled', 'Cancelled'),
	]

	patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
	doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
	date = models.DateField()
	time = models.TimeField()
	reason = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('doctor', 'date', 'time')
		ordering = ['date', 'time']

	def __str__(self) -> str:
		return f"Appointment: {self.patient.user.username} with {self.doctor.user.username} on {self.date} at {self.time} ({self.status})"

