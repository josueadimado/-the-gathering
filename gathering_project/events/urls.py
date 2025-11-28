from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('create/', views.event_create, name='create'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('<int:pk>/update/', views.event_update, name='update'),
    path('<int:pk>/delete/', views.event_delete, name='delete'),
    path('<int:pk>/qr-code/', views.event_qr_code, name='qr_code'),
    path('<int:pk>/qr-scan/', views.event_qr_scan, name='qr_scan'),
]

