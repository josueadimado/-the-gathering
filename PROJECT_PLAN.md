# The Gathering - Detailed Project Plan

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Database Design](#database-design)
4. [Module Breakdown](#module-breakdown)
5. [Development Phases](#development-phases)
6. [Technical Considerations](#technical-considerations)
7. [Dependencies & Integrations](#dependencies--integrations)

---

## Project Overview

### What We're Building
A web-based system for "The Gathering" that helps manage:
- **Public Registration**: People can sign up without creating accounts
- **Event Management**: Create and manage weekly gatherings and special events
- **Attendance Tracking**: Check people in using QR codes or by searching their name
- **Automated Reminders**: Send WhatsApp/SMS reminders before events
- **Feedback Collection**: Collect suggestions and prayer requests
- **Analytics Dashboard**: Show leaders statistics and insights

### Key Requirements
- **No Login Required for Public**: Regular attendees don't need accounts
- **Admin Access**: Only administrators need to log in
- **QR Code Support**: Fast check-in using QR codes
- **Messaging Integration**: Connect with WhatsApp/SMS services
- **Mobile-Friendly**: Works well on phones and tablets

---

## Technology Stack

### Backend Framework: Django
**What is Django?**
- Django is a Python web framework (a toolkit for building websites)
- It handles database operations, user authentication, and web pages
- It's secure, well-documented, and widely used

**Why Django?**
- Built-in admin panel (perfect for managing events and people)
- Strong security features
- Easy database management
- Great for building complex web applications

### Database: SQLite (Development) / PostgreSQL (Production)
**What is a Database?**
- A database stores information (like names, events, attendance records)
- Think of it like a digital filing cabinet

**SQLite vs PostgreSQL:**
- **SQLite**: Simple, file-based database (good for development/testing)
- **PostgreSQL**: More powerful database (better for production/live system)

### Frontend: Django Templates + Bootstrap
**What is Frontend?**
- The part of the website users see and interact with
- Forms, buttons, pages, etc.

**Why Django Templates + Bootstrap?**
- Django Templates: Built-in way to create web pages in Django
- Bootstrap: CSS framework that makes websites look modern and mobile-friendly

### Messaging Services (To Be Integrated)
- **WhatsApp Business API** or **Twilio** (for SMS/WhatsApp)
- We'll need API credentials from these services

---

## Database Design

### Core Tables (Models)

#### 1. **Person** (People Module)
Stores information about registered attendees
```
- id: Unique identifier
- first_name: Person's first name
- last_name: Person's last name
- phone_number: For sending reminders
- email: Optional email address
- date_registered: When they first registered
- is_active: Whether they're still attending
- qr_code: Unique QR code identifier (for future use)
```

#### 2. **Event** (Events Module)
Stores information about gatherings/meetings
```
- id: Unique identifier
- name: Event name (e.g., "Sunday Service")
- event_date: When the event happens
- event_time: What time it starts
- event_type: Weekly gathering, special event, etc.
- location: Where it's held
- is_active: Whether event is still happening
- created_at: When event was created
```

#### 3. **Attendance** (Attendance Module)
Records who attended which events
```
- id: Unique identifier
- person: Link to Person (who attended)
- event: Link to Event (which event)
- check_in_time: When they checked in
- check_in_method: QR code, manual search, etc.
- checked_in_by: Which admin checked them in
```

#### 4. **Feedback** (Feedback Module)
Stores suggestions and prayer requests
```
- id: Unique identifier
- person: Link to Person (optional - can be anonymous)
- feedback_type: Suggestion, prayer request, etc.
- message: The actual feedback text
- submitted_at: When it was submitted
- is_anonymous: Whether person wants to remain anonymous
- status: New, reviewed, addressed, etc.
```

#### 5. **MessageTemplate** (Messaging Module)
Stores reusable message templates
```
- id: Unique identifier
- name: Template name (e.g., "Event Reminder")
- message_type: SMS, WhatsApp, Email
- subject: Message subject (if email)
- body: Message content
- variables: Placeholders like {name}, {event_date}
```

#### 6. **MessageLog** (Messaging Module)
Tracks sent messages
```
- id: Unique identifier
- person: Who received the message
- event: Related event (if applicable)
- template: Which template was used
- message_type: SMS, WhatsApp, Email
- status: Sent, failed, pending
- sent_at: When it was sent
- error_message: If sending failed
```

#### 7. **User** (Accounts Module - Django Built-in)
Django's built-in user system for admins
```
- username: Admin login username
- email: Admin email
- password: Encrypted password
- is_staff: Can access admin panel
- is_superuser: Full admin access
```

---

## Module Breakdown

### Module 1: Accounts
**Purpose**: Handle admin user authentication and permissions

**Features**:
- Admin login/logout
- Password reset
- User permissions (who can do what)
- Admin dashboard access control

**Files Needed**:
- `accounts/models.py` - User extensions (if needed)
- `accounts/views.py` - Login/logout views
- `accounts/urls.py` - URL routes
- `accounts/templates/` - Login pages

---

### Module 2: People
**Purpose**: Manage public registration without requiring accounts

**Features**:
- Public registration form (no login needed)
- View/edit person details (admin only)
- Search people by name/phone
- Generate QR codes (future enhancement)
- List all registered people

**Files Needed**:
- `people/models.py` - Person model
- `people/views.py` - Registration and management views
- `people/forms.py` - Registration form
- `people/urls.py` - URL routes
- `people/templates/` - Registration form, person list

**Key Views**:
1. **Public Registration**: Simple form anyone can fill out
2. **Person Search**: Admin searches for people
3. **Person Detail**: View/edit person information

---

### Module 3: Events
**Purpose**: Create and manage events/gatherings

**Features**:
- Create new events
- Edit existing events
- List upcoming/past events
- Event calendar view
- Delete/cancel events

**Files Needed**:
- `events/models.py` - Event model
- `events/views.py` - CRUD operations (Create, Read, Update, Delete)
- `events/forms.py` - Event creation/edit form
- `events/urls.py` - URL routes
- `events/templates/` - Event pages

**Key Views**:
1. **Event List**: Show all events
2. **Create Event**: Form to add new event
3. **Event Detail**: View event info and attendance
4. **Edit Event**: Modify event details

---

### Module 4: Attendance
**Purpose**: Track who attends which events

**Features**:
- QR code check-in (scan QR code to check in)
- Manual check-in (search by name)
- View attendance for an event
- View person's attendance history
- Export attendance reports

**Files Needed**:
- `attendance/models.py` - Attendance model
- `attendance/views.py` - Check-in views
- `attendance/forms.py` - Check-in forms
- `attendance/urls.py` - URL routes
- `attendance/templates/` - Check-in interface
- `attendance/qr_scanner.py` - QR code scanning logic

**Key Views**:
1. **Check-In Page**: Main check-in interface (QR + search)
2. **Attendance List**: Who attended a specific event
3. **Person History**: One person's attendance record

**Technical Notes**:
- QR codes can be generated using Python libraries (qrcode, pyqrcode)
- QR scanner can use webcam via JavaScript libraries
- QR code contains person ID or unique identifier

---

### Module 5: Feedback
**Purpose**: Collect suggestions and prayer requests

**Features**:
- Public feedback form (no login)
- Submit prayer requests
- Submit suggestions
- Anonymous option
- Admin view/manage feedback
- Mark feedback as reviewed/addressed

**Files Needed**:
- `feedback/models.py` - Feedback model
- `feedback/views.py` - Submit and manage feedback
- `feedback/forms.py` - Feedback form
- `feedback/urls.py` - URL routes
- `feedback/templates/` - Feedback form and list

**Key Views**:
1. **Submit Feedback**: Public form
2. **Feedback List**: Admin view all feedback
3. **Feedback Detail**: View and manage specific feedback

---

### Module 6: Messaging
**Purpose**: Send automated reminders via WhatsApp/SMS

**Features**:
- Create message templates
- Schedule automatic reminders (e.g., 1 day before event)
- Send messages manually
- View message history/logs
- Track delivery status

**Files Needed**:
- `messaging/models.py` - Template and Log models
- `messaging/views.py` - Template management, send messages
- `messaging/forms.py` - Template form
- `messaging/urls.py` - URL routes
- `messaging/templates/` - Template management pages
- `messaging/services.py` - Integration with WhatsApp/SMS API
- `messaging/tasks.py` - Scheduled tasks (using Celery or Django background tasks)

**Key Views**:
1. **Template List**: View all message templates
2. **Create Template**: Add new template
3. **Send Messages**: Manual sending interface
4. **Message Logs**: View sent messages

**Technical Notes**:
- Need to integrate with WhatsApp Business API or Twilio
- Use Django background tasks or Celery for scheduled sending
- Template variables: {name}, {event_name}, {event_date}, etc.

---

### Module 7: Dashboard
**Purpose**: Analytics and insights for leadership

**Features**:
- Total registered people
- Event attendance statistics
- Attendance trends (charts)
- Recent feedback summary
- Upcoming events
- Most active attendees

**Files Needed**:
- `dashboard/views.py` - Analytics calculations and views
- `dashboard/urls.py` - URL routes
- `dashboard/templates/` - Dashboard pages
- `dashboard/utils.py` - Helper functions for calculations

**Key Views**:
1. **Main Dashboard**: Overview with key metrics
2. **Attendance Analytics**: Detailed attendance charts
3. **People Analytics**: Registration trends

**Technical Notes**:
- Use Chart.js or similar for visualizations
- Calculate statistics from database queries
- Show weekly/monthly trends

---

## Development Phases

### Phase 1: Project Setup & Foundation (Week 1)
**Goal**: Get the basic Django project running

**Tasks**:
1. Set up Django project structure
2. Configure database (SQLite for now)
3. Create Django apps for each module
4. Set up basic admin panel
5. Create base templates with Bootstrap
6. Set up Git repository (version control)

**Deliverables**:
- Working Django project
- All apps created (empty but structured)
- Basic navigation menu
- Admin can log in

---

### Phase 2: Core Models & Admin (Week 2)
**Goal**: Create database structure and admin interface

**Tasks**:
1. Create Person model
2. Create Event model
3. Create Attendance model
4. Create Feedback model
5. Create MessageTemplate and MessageLog models
6. Register all models in Django admin
7. Test data entry through admin

**Deliverables**:
- All database tables created
- Admin can add/edit/delete records
- Sample data entered for testing

---

### Phase 3: People Module (Week 3)
**Goal**: Public registration and person management

**Tasks**:
1. Create public registration form
2. Create person list view (admin)
3. Create person detail/edit view
4. Create search functionality
5. Style forms with Bootstrap
6. Add form validation

**Deliverables**:
- Public can register without login
- Admin can search and manage people
- Forms look professional and work on mobile

---

### Phase 4: Events Module (Week 4)
**Goal**: Event creation and management

**Tasks**:
1. Create event list view
2. Create event creation form
3. Create event detail view
4. Create event edit/delete functionality
5. Add event calendar view (optional)
6. Filter events (upcoming, past, all)

**Deliverables**:
- Admin can create and manage events
- Events display nicely
- Can filter by date/type

---

### Phase 5: Attendance Module (Week 5-6)
**Goal**: Check-in functionality

**Tasks**:
1. Create check-in interface
2. Implement manual search check-in
3. Add QR code generation for people
4. Implement QR code scanning (webcam)
5. Create attendance list view
6. Add attendance history per person
7. Test check-in flow

**Deliverables**:
- Can check in people via search
- Can check in via QR code scan
- View attendance records
- QR codes work reliably

---

### Phase 6: Feedback Module (Week 7)
**Goal**: Collect feedback and prayer requests

**Tasks**:
1. Create public feedback form
2. Add anonymous option
3. Create admin feedback list
4. Add status management (new, reviewed, addressed)
5. Filter feedback by type/status
6. Style feedback forms

**Deliverables**:
- Public can submit feedback
- Admin can view and manage feedback
- Anonymous submissions work

---

### Phase 7: Messaging Module (Week 8-9)
**Goal**: Automated reminders

**Tasks**:
1. Create message template system
2. Integrate WhatsApp/SMS API (Twilio or WhatsApp Business)
3. Create manual send interface
4. Set up scheduled tasks (Celery or Django background tasks)
5. Create message log view
6. Add template variables ({name}, {event_date}, etc.)
7. Test message sending

**Deliverables**:
- Can create message templates
- Can send messages manually
- Automatic reminders work
- Message logs track everything

---

### Phase 8: Dashboard Module (Week 10)
**Goal**: Analytics and insights

**Tasks**:
1. Create dashboard main page
2. Calculate key metrics (total people, attendance rates, etc.)
3. Add charts (attendance trends, registration trends)
4. Create attendance analytics page
5. Add export functionality (CSV/Excel)
6. Style dashboard professionally

**Deliverables**:
- Dashboard shows key statistics
- Charts visualize trends
- Can export data
- Looks professional

---

### Phase 9: Testing & Polish (Week 11)
**Goal**: Fix bugs and improve user experience

**Tasks**:
1. Test all features end-to-end
2. Fix bugs
3. Improve mobile responsiveness
4. Add error handling
5. Improve form validation
6. Add loading indicators
7. Optimize database queries
8. Security review

**Deliverables**:
- System works smoothly
- Mobile-friendly
- Secure
- User-friendly

---

### Phase 10: Deployment Preparation (Week 12)
**Goal**: Get ready to launch

**Tasks**:
1. Set up production database (PostgreSQL)
2. Configure production settings
3. Set up static file serving
4. Set up domain/hosting
5. Deploy to server
6. Test in production environment
7. Create user documentation

**Deliverables**:
- System running in production
- Documentation for users
- Backup strategy in place

---

## Technical Considerations

### Security
- **CSRF Protection**: Django has built-in CSRF protection (prevents form hijacking)
- **SQL Injection**: Django ORM prevents SQL injection (automatic)
- **Password Hashing**: Django automatically hashes passwords
- **Admin Access**: Only staff users can access admin
- **Input Validation**: Validate all form inputs

### Performance
- **Database Indexing**: Add indexes on frequently searched fields (name, phone, event_date)
- **Query Optimization**: Use select_related() and prefetch_related() to reduce database queries
- **Caching**: Cache dashboard statistics (update every hour, not every page load)
- **Pagination**: Show 20-50 records per page, not all at once

### Mobile Responsiveness
- **Bootstrap**: Use Bootstrap's responsive grid system
- **Touch-Friendly**: Make buttons and forms easy to tap on mobile
- **QR Scanner**: Ensure QR scanner works on mobile cameras
- **Test on Devices**: Test on actual phones, not just browser resize

### Scalability
- **Database**: Start with SQLite, move to PostgreSQL when needed
- **File Storage**: Use cloud storage (AWS S3, etc.) for QR code images if needed
- **Background Tasks**: Use Celery for scheduled messaging (handles many messages)
- **CDN**: Use CDN for static files if traffic grows

---

## Dependencies & Integrations

### Python Packages Needed
```
Django==4.2.x          # Web framework
Pillow                 # Image handling (for QR codes)
qrcode                 # Generate QR codes
pyqrcode               # QR code utilities
celery                 # Background tasks (for scheduled messages)
django-celery-beat     # Schedule tasks
twilio                 # SMS/WhatsApp API (if using Twilio)
requests               # HTTP requests (for API calls)
python-decouple        # Environment variables management
```

### External Services Needed
1. **Messaging Service**:
   - Option A: Twilio (SMS and WhatsApp)
   - Option B: WhatsApp Business API
   - Need: API credentials (account SID, auth token)

2. **Hosting** (for production):
   - Option A: Heroku (easy, paid)
   - Option B: DigitalOcean (more control)
   - Option C: AWS (scalable, complex)
   - Need: Server, domain name

3. **Database** (for production):
   - PostgreSQL (free tier available on many platforms)

### API Integrations
- **WhatsApp/SMS API**: Send messages
- **QR Code Generation**: Create QR codes (local, no API needed)
- **QR Code Scanning**: Use device camera (JavaScript library)

---

## Questions to Consider

### Before Starting Development:
1. **Messaging Service**: Which service will you use? (Twilio, WhatsApp Business API, other?)
2. **Hosting**: Where will the system be hosted? (affects deployment approach)
3. **QR Codes**: Will each person have a permanent QR code, or generate per event?
4. **Reminder Timing**: How many days/hours before event should reminders be sent?
5. **Admin Access**: How many admins will there be? Need different permission levels?
6. **Data Privacy**: Any specific privacy requirements? (GDPR, etc.)

### During Development:
1. **Testing**: Will you need automated tests? (recommended but adds time)
2. **Backup**: How often should database be backed up?
3. **Notifications**: Should admins get notified of new feedback/registrations?

---

## Next Steps

1. **Review this plan** - Does it cover everything you need?
2. **Answer questions** - Fill in the "Questions to Consider" section
3. **Set up development environment** - Install Python, Django, etc.
4. **Start Phase 1** - Begin project setup

---

## Glossary (For Beginners)

- **Model**: A database table structure (like a blueprint)
- **View**: Code that handles web page requests and responses
- **Template**: HTML file that displays information
- **URL Route**: Maps web addresses to views
- **Form**: Web form for users to enter data
- **Admin Panel**: Built-in Django interface for managing data
- **API**: Application Programming Interface (way for programs to talk to each other)
- **ORM**: Object-Relational Mapping (Django's way of talking to databases)
- **Migration**: Updates database structure when models change
- **Static Files**: CSS, JavaScript, images (files that don't change)
- **Middleware**: Code that runs on every request (like security checks)

---

**Last Updated**: [Current Date]
**Status**: Planning Phase
**Next Review**: After answering questions and confirming approach

