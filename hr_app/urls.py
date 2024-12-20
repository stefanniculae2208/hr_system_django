from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_employee, name='add_employee'),
    path('employee/<int:pk>/', views.get_employee_by_id, name='get_employee_by_id'),
    path('employees/', views.get_all_employees, name='get_all_employees'),
    path('employee/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('employee/update/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees_filtered/', views.employees_filtered, name='employees_filtered'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    path('upload_employees/', views.upload_employees, name='upload_employees'),
]