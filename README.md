# The Gathering - Django Project

This is the Django project folder for The Gathering Attendance & Messaging System.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (create `.env` file):
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run server**:
   ```bash
   python manage.py runserver
   ```

6. **Access admin panel**:
   ```
   http://127.0.0.1:8000/admin/
   ```

## Project Structure

- `gathering_project/` - Main Django project configuration
- `accounts/` - Admin authentication
- `people/` - Public registration
- `events/` - Event management
- `attendance/` - Check-in system
- `feedback/` - Feedback collection
- `messaging/` - Message templates & sending
- `dashboard/` - Analytics dashboard
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, images
- `media/` - User uploaded files

## Documentation

- See `../SETUP.md` for detailed setup instructions
- See `../PROJECT_PLAN.md` for complete project specifications
- See `../QUICK_REFERENCE.md` for quick reference guide

