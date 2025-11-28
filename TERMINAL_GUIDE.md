# Terminal Guide - How to Access and Use Terminal

## 🖥️ How to Open Terminal on Mac

### Method 1: Using Spotlight Search
1. Press `Command + Space` (⌘ + Space)
2. Type "Terminal"
3. Press `Enter`

### Method 2: Using Finder
1. Open Finder
2. Go to **Applications** → **Utilities**
3. Double-click on **Terminal**

### Method 3: Using Launchpad
1. Press `F4` or swipe with 4 fingers on trackpad
2. Type "Terminal"
3. Click on Terminal icon

---

## 📝 Basic Terminal Commands You'll Need

### Navigate to Your Project
```bash
cd "/Users/josueadimado/Documents/The Gathering"
```

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Go to Django Project Folder
```bash
cd gathering_project
```

---

## 🚀 Quick Start Commands

### Option 1: Use the Startup Script (Easiest!)
1. Open Terminal
2. Run this command:
```bash
cd "/Users/josueadimado/Documents/The Gathering" && chmod +x start_server.sh && ./start_server.sh
```

### Option 2: Manual Steps

**Step 1: Navigate to project**
```bash
cd "/Users/josueadimado/Documents/The Gathering"
```

**Step 2: Activate virtual environment**
```bash
source venv/bin/activate
```

**Step 3: Go to Django project**
```bash
cd gathering_project
```

**Step 4: Create admin user (first time only)**
```bash
python manage.py createsuperuser
```
Follow the prompts to create username, email, and password.

**Step 5: Start the server**
```bash
python manage.py runserver
```

---

## 🌐 Accessing Your Application

Once the server is running, you'll see:
```
Starting development server at http://127.0.0.1:8000/
```

### Open in Browser:
1. Open any web browser (Chrome, Safari, Firefox)
2. Go to: `http://127.0.0.1:8000/admin/`
3. Log in with your superuser credentials

---

## 🛑 Stopping the Server

When you want to stop the server:
1. Click in the Terminal window
2. Press `Ctrl + C`
3. The server will stop

---

## 📋 Common Commands Reference

### Check if server is running
```bash
ps aux | grep "manage.py runserver"
```

### Create database migrations (after changing models)
```bash
cd "/Users/josueadimado/Documents/The Gathering"
source venv/bin/activate
cd gathering_project
python manage.py makemigrations
python manage.py migrate
```

### Access Django shell (for testing)
```bash
cd "/Users/josueadimado/Documents/The Gathering"
source venv/bin/activate
cd gathering_project
python manage.py shell
```

### Collect static files
```bash
cd "/Users/josueadimado/Documents/The Gathering"
source venv/bin/activate
cd gathering_project
python manage.py collectstatic
```

---

## 💡 Tips

1. **Always activate virtual environment first** - You'll see `(venv)` in your terminal prompt when it's active
2. **Keep terminal open** - The server runs in the terminal, so keep it open while using the app
3. **Check for errors** - If something doesn't work, check the terminal for error messages
4. **Use Tab key** - Press Tab to auto-complete file/folder names

---

## 🆘 Troubleshooting

### "Command not found"
- Make sure you've activated the virtual environment: `source venv/bin/activate`

### "Port already in use"
- Another server might be running. Stop it first or use a different port:
```bash
python manage.py runserver 8001
```

### "No module named django"
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

---

## 📞 Need Help?

If you're stuck:
1. Check the terminal for error messages (they're usually helpful!)
2. Make sure virtual environment is activated
3. Verify you're in the correct directory
4. Check SETUP.md for detailed instructions

