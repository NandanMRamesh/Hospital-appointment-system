from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PatientProfile, DoctorProfile


class AuthRedirectTests(TestCase):
	def setUp(self):
		# create a patient user
		self.patient_user = User.objects.create_user(username='patient1', password='pass')
		PatientProfile.objects.create(user=self.patient_user)

		# create a doctor user
		self.doctor_user = User.objects.create_user(username='doctor1', password='pass')
		DoctorProfile.objects.create(user=self.doctor_user)

	def test_patient_login_redirects_to_patient_dashboard(self):
		resp = self.client.post(reverse('login'), {'username': 'patient1', 'password': 'pass'})
		self.assertRedirects(resp, reverse('patient_dashboard'))

	def test_doctor_login_redirects_to_doctor_dashboard(self):
		resp = self.client.post(reverse('login'), {'username': 'doctor1', 'password': 'pass'})
		self.assertRedirects(resp, reverse('doctor_dashboard'))

	def test_logout_post_logs_out(self):
		# login first
		self.client.login(username='patient1', password='pass')
		resp = self.client.post(reverse('logout'))
		# should redirect to home
		self.assertRedirects(resp, reverse('home'))
