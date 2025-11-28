from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Public self-service check-in
    path('self-check-in/', views.self_check_in, name='self_check_in'),
    
    # Admin check-in (requires login)
    path('check-in/', views.check_in, name='check_in'),
    path('check-in/qr/', views.check_in_qr, name='check_in_qr'),
    path('search/', views.search_person, name='search_person'),
    path('', views.attendance_list, name='list'),
    path('event/<int:event_id>/', views.attendance_list, name='list_by_event'),
    path('person/<uuid:person_id>/', views.person_attendance_history, name='person_history'),
]

