from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('register/', views.register, name='register'),  # Public registration
    path('register/success/', views.register_success, name='register_success'),
    path('admin/register/', views.admin_register, name='admin_register'),  # Admin registration
    path('import/', views.import_excel, name='import_excel'),  # Excel import
    path('list/', views.person_list, name='list'),
    path('<uuid:pk>/', views.person_detail, name='detail'),
    path('<uuid:pk>/update/', views.person_update, name='update'),
]

