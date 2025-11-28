# Setup Guide - The Gathering Project

This guide will help you set up the Django project on your computer.

## Prerequisites

Before starting, make sure you have:
- **Python 3.8 or higher** installed
- **pip** (Python package installer) - comes with Python
- **Git** (optional, for version control)

## Step 1: Install Python Dependencies

1. Open your terminal/command prompt
2. Navigate to the project folder:
   ```bash
   cd "/Users/josueadimado/Documents/The Gathering"
   ```

3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - **On Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```

5. Install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Set Up Environment Variables

1. Create a `.env` file in the project root (copy from `.env.example` if it exists, or create new):
   ```bash
   touch .env
   ```

2. Add the following to your `.env` file:
   ```
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   **Note:** Generate a secret key by running:
   ```bash
   python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

## Step 3: Set Up the Database

1. Navigate to the Django project folder:
   ```bash
   cd gathering_project
   ```

2. Create database migrations:
   ```bash
   python manage.py makemigrations
   ```

3. Apply migrations to create database tables:
   ```bash
   python manage.py migrate
   ```

## Step 4: Create a Superuser (Admin Account)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin username, email, and password.

## Step 5: Collect Static Files

Collect static files (CSS, JavaScript) for the admin panel:

```bash
python manage.py collectstatic --noinput
```

## Step 6: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
```

## Step 7: Access the Application

1. **Admin Panel**: Open your browser and go to:
   ```
   http://127.0.0.1:8000/admin/
   ```
   Log in with the superuser credentials you created.

2. **Main Application**: Go to:
   ```
   http://127.0.0.1:8000/
   ```
   This will redirect to the dashboard (you'll need to log in first).

## Troubleshooting

### Issue: "Django not found" or "No module named django"
**Solution**: Make sure you activated the virtual environment and installed requirements:
```bash
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution**: Run the server on a different port:
```bash
python manage.py runserver 8001
```

### Issue: Database errors
**Solution**: Make sure you ran migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

## Adding Images to Login Page

To add images (logo, background, etc.) to the login page:

1. **Image Location**: Put your images in:
   ```
   gathering_project/static/images/login/
   ```

2. **Recommended Images**:
   - `logo.png` - Main logo (200x200px to 400x400px, PNG with transparency)
   - `background.jpg` - Background image (1920x1080px or larger, JPG)
   - `side-image.jpg` - Side panel image (800x1200px, JPG)

3. **After adding images**, inform the developer with:
   - Image file names you added
   - What each image is (logo, background, etc.)

## Next Steps

After setup is complete:

1. **Log into the admin panel** and explore the models
2. **Create some test data**:
   - Add a few people through the admin
   - Create an event
   - Test the registration form
3. **Start building templates** - The views are ready, but templates need to be created
4. **Configure messaging API** - Set up Twilio or WhatsApp Business API credentials
5. **Add images** - Place images in `gathering_project/static/images/login/` for login page customization

## Project Structure

```
gathering_project/
├── gathering_project/     # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── accounts/              # Admin authentication
├── people/                # Public registration
├── events/                # Event management
├── attendance/            # Check-in system
├── feedback/              # Feedback collection
├── messaging/             # Message templates & sending
├── dashboard/             # Analytics dashboard
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # User uploaded files
└── manage.py             # Django management script
```

## Development Tips

1. **Always activate your virtual environment** before working on the project
2. **Run migrations** whenever you change models
3. **Check the terminal** for error messages - Django shows helpful debug info
4. **Use the admin panel** to quickly add test data
5. **Check Django documentation** at https://docs.djangoproject.com/ if you get stuck

## Getting Help

- Django Documentation: https://docs.djangoproject.com/
- Django Tutorial: https://docs.djangoproject.com/en/4.2/intro/tutorial01/
- Check PROJECT_PLAN.md for detailed project specifications

---

**Happy Coding! 🎉**

