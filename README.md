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

---

## Customizing UI (CSS & images)

Static assets are under `app/static/`:

- CSS: `app/static/css/style.css` — primary place for custom styles.
- Images: `app/static/images/` — placeholder images live here.

To replace placeholders:
1. Put your images into `app/static/images/` with the same filenames (or update template paths).
2. Recommended sizes:
   - Hero: around 1200x600 (or SVG for scalability)
   - Card icons: 64x64 or 128x128

If you change filenames, update the templates (e.g., `app/templates/home.html`) accordingly.

To add more styles:
- Edit `app/static/css/style.css`.
- For major additions, create new CSS files and include them in `app/templates/base.html` using the `{% static %}` tag.

Tip: during development Chrome/Edge may cache CSS. Use hard-refresh or disable cache in dev tools while developing.

---

## Extending booking slots

Currently the app exposes a simple set of slots (9:00–16:00 hourly). To make slots per-doctor:

1. Add fields to `DoctorProfile` for working hours/slot duration.
2. Update `AvailableSlotsView` to generate slots according to doctor's schedule.
3. Add UI to the doctor profile form so admins can edit availability.

Consider race conditions: when two patients request the same slot concurrently, wrap booking in a transaction and re-check availability just before saving.

---

## Tests

Run tests:

```powershell
python manage.py test app
```

The project includes tests for login redirects and logout behavior.

Add more tests for booking and slot conflict handling as you extend the app.

---

## Security & deployment notes

This project is configured for local development. Before deploying to production, address the following:

- Set `DEBUG = False` in `proj/settings.py`.
- Use a strong `SECRET_KEY` stored in an environment variable: `DJANGO_SECRET_KEY`.
- Configure `ALLOWED_HOSTS`.
- Enable secure cookie settings:
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
- Consider `SECURE_HSTS_SECONDS` and `SECURE_SSL_REDIRECT` when serving over HTTPS.

Use a production WSGI/ASGI server (e.g., Gunicorn, Daphne) and serve static files via a CDN or web server.

---

## Development tips

- Use `python manage.py runserver` for development.
- To inspect the DB quickly, use SQLite browser on `db.sqlite3`.
- To create doctors, use the Django admin: http://127.0.0.1:8000/admin/ (superuser required).
- Add feature branches, and keep migrations under version control.

---

## Troubleshooting

- `no such table` errors usually mean migrations weren't applied:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- `NoReverseMatch` for a URL name usually means the named URL doesn't exist; check `app/urls.py` and templates.

- For static files not appearing: ensure `STATICFILES_DIRS` in `proj/settings.py` is correct and that `collectstatic` is used for production.

---

## Next improvements you might want

- Implement per-doctor availability and slot durations.
- Add email notifications for appointment confirmations.
- Add pagination and filtering for long appointment lists.
- Add better error reporting and monitoring for production.

---

If you want, I can also:
- Add more polished default images and icons.
- Add a simple responsive UI kit (e.g., integrate Tailwind or Bootstrap theme).
- Implement per-doctor schedules and atomic booking to prevent race conditions.

Tell me which of those you'd like next and I'll implement it.
