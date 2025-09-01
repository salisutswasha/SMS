# filepath: c:\Users\HP\Desktop\sarzee\schoolmanagement-master\schoolmanagement-master\school\urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Example:
    # path('', views.home_view, name='home'),
    path('admin-edit-teacher-salary/<int:pk>/', views.admin_edit_teacher_salary_view, name='admin-edit-teacher-salary'),
]