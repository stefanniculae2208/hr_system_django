from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_employee, name='add_employee'),
    path('employee/<int:pk>/', views.get_employee_by_id, name='get_employee_by_id'),
    path('employees/', views.get_all_employees, name='get_all_employees'),
    path('employee/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('employee/update/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees_filtered/', views.employees_filtered, name='employees_filtered'),
    path('average_age_by_industry/', views.average_age_by_industry, name='average_age_by_industry'),
    path('average_salary_by_industry/', views.average_salary_by_industry, name='average_salary_by_industry'),
    path('average_salary_by_experience/', views.average_salary_by_experience, name='average_salary_by_experience'),
    path('gender_distribution_per_industry/', views.gender_distribution_per_industry, name='gender_distribution_per_industry'),
    path('percentage_above_threshold/', views.percentage_above_threshold, name='percentage_above_threshold'),
    path('upload_employees/', views.upload_employees, name='upload_employees'),
]