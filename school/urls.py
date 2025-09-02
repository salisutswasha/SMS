# filepath: school/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin-edit-teacher-salary/<int:pk>/', views.admin_edit_teacher_salary_view, name='admin-edit-teacher-salary'),
    path('admin-view-student-fee/', views.admin_view_student_fee_all_view, name='admin-view-student-fee-all'),
    path('admin-view-student-fee/<str:cl>', views.admin_view_student_fee_view, name='admin-view-student-fee'),
    path('admin-edit-student-fee/<int:pk>/', views.admin_edit_student_fee_view, name='admin-edit-student-fee'),

    path('login/', views.custom_login_view, name='login'),
    path('studentlogin', views.student_login_view, name='studentlogin'),
    path('teacherlogin', views.teacher_login_view, name='teacherlogin'),
    path('adminlogin', views.admin_login_view, name='adminlogin'),

    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('studentsignup/', views.student_signup_view, name='studentsignup'),
    path('teachersignup/', views.teacher_signup_view, name='teachersignup'),
]
