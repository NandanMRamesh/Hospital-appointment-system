# Hospital Appointment System

This is a simple Django application for managing hospital appointments. It supports patient registration and login, booking appointments with doctors, doctor dashboard, and admin management.

This README covers setup, development, deployment hints, and project-specific notes so you can modify and extend the project.

---

## Quick start (local development)

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If `requirements.txt` is not provided, at minimum install Django:

```powershell
pip install Django
```

2. Run migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

3. Start the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

---

## Project structure (important files)

- `manage.py` - Django management script.
- `proj/` - Django project settings and root `urls.py`.
- `app/` - Main application code.
  - `models.py` - `PatientProfile`, `DoctorProfile`, `Appointment` models.
  - `views.py` - Class-based views (home, registration, booking, dashboards, AJAX slots, completion action).
  - `forms.py` - `PatientRegistrationForm`, `AppointmentForm` (with conflict validation).
  - `templates/` - HTML templates for pages.
  - `static/` - Static files: `css/`, `images/`.
  - `tests.py` - Unit tests for auth redirects and logout.

---

## Key features implemented

- Patient registration/login flow.
- Doctor accounts created via Django admin (admin-only).
- Patient dashboard with upcoming appointments.
- Doctor dashboard with appointments and ability to mark appointments as Completed.
- Booking flow with AJAX-driven available time slots per doctor and date.
- Success/error messages using Django messages.
- Role-aware login redirect: patients → `/patient/dashboard/`, doctors → `/doctor/dashboard/`, staff → Django admin.
- Unit tests for role-aware redirects and logout.

## Troubleshooting

- `no such table` errors usually mean migrations weren't applied:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- `NoReverseMatch` for a URL name usually means the named URL doesn't exist; check `app/urls.py` and templates.

- For static files not appearing: ensure `STATICFILES_DIRS` in `proj/settings.py` is correct and that `collectstatic` is used for production.

---
