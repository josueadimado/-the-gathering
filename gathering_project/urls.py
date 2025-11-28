"""
URL configuration for gathering_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Public landing page
    path('', views.landing, name='landing'),
    
    # App URLs
    path('dashboard/', include('dashboard.urls')),  # Dashboard requires login
    path('accounts/', include('accounts.urls')),
    path('people/', include('people.urls')),
    path('events/', include('events.urls')),
    path('attendance/', include('attendance.urls')),
    path('feedback/', include('feedback.urls')),
    path('messaging/', include('messaging.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

