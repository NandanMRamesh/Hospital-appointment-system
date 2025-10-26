from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientProfile, DoctorProfile, Appointment
from django.utils import timezone


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        PatientProfile.objects.get_or_create(user=user, defaults={
            'phone': self.cleaned_data.get('phone', ''),
            'date_of_birth': self.cleaned_data.get('date_of_birth')
        })
        return user


class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    specialization = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        DoctorProfile.objects.get_or_create(user=user, defaults={
            'specialization': self.cleaned_data.get('specialization', ''),
            'phone': self.cleaned_data.get('phone', '')
        })
        return user


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'time', 'reason')

    def clean(self):
        cleaned = super().clean()
        doctor = cleaned.get('doctor')
        date = cleaned.get('date')
        time = cleaned.get('time')

        if date and date < timezone.localdate():
            raise forms.ValidationError('Appointment date cannot be in the past.')

        if doctor and date and time:
            conflict = Appointment.objects.filter(doctor=doctor, date=date, time=time).exists()
            if conflict:
                raise forms.ValidationError('The selected doctor already has an appointment at this date and time.')

        return cleaned
