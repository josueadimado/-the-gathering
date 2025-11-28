#!/bin/bash
# Startup script for The Gathering Django project

echo "🚀 Starting The Gathering Django Server..."
echo ""

# Navigate to project directory
cd "/Users/josueadimado/Documents/The Gathering"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Navigate to Django project
cd gathering_project

# Check if migrations are up to date
echo "🔍 Checking database..."
python manage.py migrate

# Start the server
echo ""
echo "✅ Starting Django development server..."
echo "🌐 Server will be available at: http://127.0.0.1:8000/"
echo "🔐 Admin panel: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

