from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .forms import PatientRegistrationForm, AppointmentForm
from .models import DoctorProfile, PatientProfile, Appointment


class HomeView(TemplateView):
	template_name = 'home.html'

	def dispatch(self, request, *args, **kwargs):
		# If user is authenticated, redirect to their dashboard based on role
		user = request.user
		if user.is_authenticated:
			if hasattr(user, 'patient_profile'):
				return redirect('patient_dashboard')
			if hasattr(user, 'doctor_profile'):
				return redirect('doctor_dashboard')
			if user.is_staff or user.is_superuser:
				return redirect('admin:index')
		return super().dispatch(request, *args, **kwargs)


class PatientRegisterView(CreateView):
	form_class = PatientRegistrationForm
	template_name = 'registration/patient_register.html'
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		# Create user but do not auto-login; redirect to login so user may authenticate
		user = form.save()
		messages.success(self.request, 'Registration successful. Please log in.')
		return redirect(self.success_url)


class CustomLoginView(auth_views.LoginView):
	template_name = 'registration/login.html'

	def get_success_url(self):
		# After login, route based on role
		user = self.request.user
		if hasattr(user, 'patient_profile'):
			return reverse('patient_dashboard')
		if hasattr(user, 'doctor_profile'):
			return reverse('doctor_dashboard')
		if user.is_staff or user.is_superuser:
			return reverse('admin:index')
		return super().get_success_url()


class BookAppointmentView(LoginRequiredMixin, View):
	template_name = 'booking/book_appointment.html'

	def get(self, request):
		form = AppointmentForm()
		# Show list of doctors for selection; slots are loaded via AJAX
		doctors = DoctorProfile.objects.select_related('user').all()
		return render(request, self.template_name, {'form': form, 'doctors': doctors})

	def post(self, request):
		form = AppointmentForm(request.POST)
		if form.is_valid():
			appointment = form.save(commit=False)
			patient_profile, _ = PatientProfile.objects.get_or_create(user=request.user)
			appointment.patient = patient_profile
			appointment.save()
			messages.success(request, 'Appointment booked successfully.')
			return redirect('patient_dashboard')
		doctors = DoctorProfile.objects.select_related('user').all()
		return render(request, self.template_name, {'form': form, 'doctors': doctors})


class DoctorRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		req = getattr(self, 'request', None)
		user = getattr(req, 'user', None)
		return bool(user and hasattr(user, 'doctor_profile'))


class DoctorDashboardView(LoginRequiredMixin, DoctorRequiredMixin, ListView):
	template_name = 'doctor/dashboard.html'
	context_object_name = 'appointments'

	def get_queryset(self):
		user = getattr(self.request, 'user', None)
		if not user or not hasattr(user, 'doctor_profile'):
			return Appointment.objects.none()
		doctor = user.doctor_profile
		return Appointment.objects.filter(doctor=doctor).order_by('date', 'time')


class PatientDashboardView(LoginRequiredMixin, ListView):
	template_name = 'patient/dashboard.html'
	context_object_name = 'appointments'

	def get_queryset(self):
		patient = getattr(self.request.user, 'patient_profile', None)
		if not patient:
			return Appointment.objects.none()
		return Appointment.objects.filter(patient=patient, status='scheduled').order_by('date', 'time')


class CompleteAppointmentView(LoginRequiredMixin, View):
	def post(self, request, pk):
		appt = get_object_or_404(Appointment, pk=pk)
		# Only the doctor assigned or an admin may mark complete
		user = request.user
		if hasattr(user, 'doctor_profile') and appt.doctor == user.doctor_profile or user.is_staff:
			appt.status = 'completed'
			appt.save()
			messages.success(request, 'Appointment marked as completed.')
			# Redirect back to doctor's dashboard
			return redirect('doctor_dashboard')
		messages.error(request, 'Permission denied.')
		return redirect('home')


class AvailableSlotsView(LoginRequiredMixin, View):
	def get(self, request):
		# Expect doctor_id and date in query params
		doctor_id = request.GET.get('doctor_id')
		date = request.GET.get('date')
		if not doctor_id or not date:
			return JsonResponse({'error': 'doctor_id and date required'}, status=400)

		# parse date
		try:
			date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
		except ValueError:
			return JsonResponse({'error': 'invalid date format'}, status=400)

		# Define fixed time slots (example every hour 9..16)
		slots = [f"{h:02d}:00" for h in range(9, 17)]

		# Remove slots that already have appointments
		booked = Appointment.objects.filter(doctor_id=doctor_id, date=date_obj).values_list('time', flat=True)
		booked_str = {t.strftime('%H:%M') for t in booked}
		available = [s for s in slots if s not in booked_str]

		return JsonResponse({'slots': available})



class AdminAppointmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
	template_name = 'admin/appointments.html'
	context_object_name = 'appointments'

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get_queryset(self):
		return Appointment.objects.select_related('patient__user', 'doctor__user').order_by('date', 'time')

