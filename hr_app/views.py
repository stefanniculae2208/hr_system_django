from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import json
from datetime import datetime
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import Employee
from .serializers import EmployeeSerializer
from .utils import statistics


@api_view(['POST'])
def add_employee(request):
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # HTTP 201 Created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # HTTP 400 Bad Request


@api_view(['GET'])
def get_employee_by_id(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
def update_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    for key, value in request.data.items():
        if value is not None and hasattr(employee, key):
            setattr(employee, key, value)
    employee.save()
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


@api_view(['GET'])
def employees_filtered(request):
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    email = request.GET.get('email', None)
    industry = request.GET.get('industry', None)
    salary_min = request.GET.get('salary_min', None)
    salary_max = request.GET.get('salary_max', None)
    filter_conditions = Q()

    if first_name:
        filter_conditions &= Q(first_name__icontains=first_name)
    if last_name:
        filter_conditions &= Q(last_name__icontains=last_name)
    if email:
        filter_conditions &= Q(email__icontains=email)
    if industry:
        filter_conditions &= Q(industry__icontains=industry)
    if salary_min:
        filter_conditions &= Q(salary__gte=salary_min)
    if salary_max:
        filter_conditions &= Q(salary__lte=salary_max)

    employees = Employee.objects.filter(filter_conditions)
    sort_by = request.GET.get('sort_by', None)
    if sort_by:
        employees = employees.order_by(sort_by)

    paginator = PageNumberPagination()
    paginated_employees = paginator.paginate_queryset(employees, request)
    serializer = EmployeeSerializer(paginated_employees, many=True)
    return paginator.get_paginated_response(serializer.data)


def get_statistics(request):
    function_map = {
        'average_age_by_industry': statistics.average_age_by_industry,
        'average_salary_by_industry': statistics.average_salary_by_industry,
        'average_salary_by_experience': statistics.average_salary_by_experience,
        'gender_distribution_per_industry': statistics.gender_distribution_per_industry,
        'percentage_above_threshold': statistics.percentage_above_threshold,
    }
    stat = request.GET.get('stat')
    if not stat:
        return HttpResponseBadRequest("Missing 'stat' parameter")
    func = function_map.get(stat)
    if not func:
        return HttpResponseBadRequest(f"Invalid 'stat' value: {stat}")
    return func(request)


@csrf_exempt
def upload_employees(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
    try:
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)
        content = uploaded_file.read()
        employees = json.loads(content)

        max_id_in_file = 0
        with transaction.atomic():
            for employee_data in employees:
                try:
                    if 'date_of_birth' in employee_data:
                        employee_data['date_of_birth'] = datetime.strptime(employee_data['date_of_birth'], "%d/%m/%Y").date()
                    #  If the added json file contains an ID column then the database autoincrement needs to be
                    # manually set to the highest value of ID in order to avoid ID overlap (since it's the unique key).
                    if 'id' in employee_data:
                        max_id_in_file = max(max_id_in_file, employee_data['id'])
                    new_employee = Employee(**employee_data)
                    new_employee.save()
                except Exception as e:
                    return JsonResponse({"error": f"Error processing employee data: {str(e)}"}, status=400)

        if max_id_in_file > 0:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('hr_app_employee', 'id'), {max_id_in_file})")
        return JsonResponse({"status": "success", "message": "Employees added successfully"})
    
    except Exception as e:
        return JsonResponse({"error": f"Error uploading file: {str(e)}"}, status=500)
