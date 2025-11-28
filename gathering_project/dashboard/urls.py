from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('attendance/', views.attendance_analytics, name='attendance_analytics'),
    path('people/', views.people_analytics, name='people_analytics'),
]

