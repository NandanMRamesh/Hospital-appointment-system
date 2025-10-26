from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import (
    HomeView,
    PatientRegisterView,
    BookAppointmentView,
    DoctorDashboardView,
    PatientDashboardView,
    AdminAppointmentListView,
    CompleteAppointmentView,
    AvailableSlotsView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/patient/', PatientRegisterView.as_view(), name='register_patient'),
    # Doctor registration is restricted to admin; do not expose a public register URL.
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('patient/dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctor/dashboard/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('appointment/<int:pk>/complete/', CompleteAppointmentView.as_view(), name='complete_appointment'),
    path('ajax/available_slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('admin/appointments/', AdminAppointmentListView.as_view(), name='admin_appointments'),
]
