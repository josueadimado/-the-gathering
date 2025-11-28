# Quick Reference Guide - The Gathering System

## 🎯 Project Summary
A Django web application for managing church/gathering attendance, registration, messaging, and feedback.

---

## 📦 Modules Overview

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **Accounts** | Admin authentication | Login, logout, permissions |
| **People** | Public registration | Registration form (no login), search, manage |
| **Events** | Event management | Create, edit, list events |
| **Attendance** | Check-in tracking | QR scan, manual search, attendance records |
| **Feedback** | Collect feedback | Prayer requests, suggestions (anonymous option) |
| **Messaging** | Automated reminders | Templates, WhatsApp/SMS, scheduled sending |
| **Dashboard** | Analytics | Statistics, charts, reports |

---

## 🗄️ Database Tables

1. **Person** - Registered attendees
2. **Event** - Gatherings/meetings
3. **Attendance** - Check-in records
4. **Feedback** - Suggestions/prayer requests
5. **MessageTemplate** - Reusable message templates
6. **MessageLog** - Sent message history
7. **User** - Admin accounts (Django built-in)

---

## 🛠️ Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Django Templates + Bootstrap
- **Messaging**: Twilio or WhatsApp Business API
- **QR Codes**: Python qrcode library
- **Charts**: Chart.js or similar

---

## 📅 Development Timeline (12 Weeks)

| Phase | Duration | Focus |
|-------|----------|-------|
| 1 | Week 1 | Project setup & foundation |
| 2 | Week 2 | Core models & admin |
| 3 | Week 3 | People module |
| 4 | Week 4 | Events module |
| 5-6 | Weeks 5-6 | Attendance module |
| 7 | Week 7 | Feedback module |
| 8-9 | Weeks 8-9 | Messaging module |
| 10 | Week 10 | Dashboard module |
| 11 | Week 11 | Testing & polish |
| 12 | Week 12 | Deployment preparation |

---

## 🔑 Key Features

### Public Features (No Login Required)
- ✅ Register for events
- ✅ Submit feedback/prayer requests
- ✅ Anonymous feedback option

### Admin Features (Login Required)
- ✅ Manage people database
- ✅ Create/edit events
- ✅ Check-in attendees (QR or search)
- ✅ View attendance records
- ✅ Manage feedback
- ✅ Create message templates
- ✅ Send reminders
- ✅ View analytics dashboard

---

## ❓ Questions to Answer Before Starting

1. **Messaging Service**: Twilio or WhatsApp Business API?
2. **Hosting**: Where will this be hosted? (Heroku, DigitalOcean, AWS?)
3. **QR Codes**: Permanent per person or generate per event?
4. **Reminder Timing**: How many days/hours before event?
5. **Admin Count**: How many admins? Need different permission levels?
6. **Privacy**: Any specific data privacy requirements?

---

## 📋 Development Checklist

### Setup Phase
- [ ] Install Python and Django
- [ ] Create Django project
- [ ] Create all app modules
- [ ] Set up database
- [ ] Configure admin panel
- [ ] Set up Bootstrap templates

### Core Development
- [ ] Create all models
- [ ] Build People module
- [ ] Build Events module
- [ ] Build Attendance module
- [ ] Build Feedback module
- [ ] Build Messaging module
- [ ] Build Dashboard module

### Integration & Testing
- [ ] Integrate messaging API
- [ ] Test QR code scanning
- [ ] Test all forms
- [ ] Test mobile responsiveness
- [ ] Security review
- [ ] Performance optimization

### Deployment
- [ ] Set up production database
- [ ] Configure production settings
- [ ] Deploy to server
- [ ] Test in production
- [ ] Create user documentation

---

## 🔗 Related Files

- **PROJECT_PLAN.md** - Full detailed plan
- **README.md** - Project overview

---

**Last Updated**: Planning Phase  
**Ready to Start?**: Review PROJECT_PLAN.md first!

