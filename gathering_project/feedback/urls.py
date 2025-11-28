from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit/', views.submit_feedback, name='submit'),
    path('submit/success/', views.submit_success, name='submit_success'),
    path('', views.feedback_list, name='list'),
    path('<int:pk>/', views.feedback_detail, name='detail'),
    path('<int:pk>/update-status/', views.feedback_update_status, name='update_status'),
]

