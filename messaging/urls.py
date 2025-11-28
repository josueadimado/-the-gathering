from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
    path('templates/<int:pk>/update/', views.template_update, name='template_update'),
    path('templates/<int:pk>/send/', views.send_message_view, name='send_message'),
    path('templates/<int:template_id>/test/', views.send_test_message, name='send_test'),
    path('logs/', views.message_log_list, name='message_log_list'),
]

