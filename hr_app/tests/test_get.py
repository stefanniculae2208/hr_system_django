from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ..models import Employee
from ..serializers import EmployeeSerializer
from decimal import Decimal
from datetime import date

class EmployeeViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url_get_by_id = '/api/hr_app/employee/{}/'
        self.url_get_all = '/api/hr_app/employees/'
        self.employee_data_1 = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'date_of_birth': date(1985, 5, 15),
            'industry': 'Software Development',
            'salary': Decimal('60000.00'),
            'years_of_experience': 10
        }
        self.employee_data_2 = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'gender': 'Female',
            'date_of_birth': date(1990, 8, 25),
            'industry': 'Marketing',
            'salary': Decimal('55000.00'),
            'years_of_experience': 8
        }
        self.employee_1 = Employee.objects.create(**self.employee_data_1)
        self.employee_2 = Employee.objects.create(**self.employee_data_2)

    @patch('hr_app.models.Employee.objects.get')
    def test_get_employee_by_id_success(self, mock_get):
        mock_get.return_value = Employee(**self.employee_data_1)
        response = self.client.get(self.url_get_by_id.format(1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.employee_data_1['first_name'])
        self.assertEqual(response.data['last_name'], self.employee_data_1['last_name'])
        mock_get.assert_called_once_with(pk=1)


    @patch('hr_app.models.Employee.objects.get')
    def test_get_employee_by_id_not_found(self, mock_get):
        mock_get.side_effect = Employee.DoesNotExist
        response = self.client.get(self.url_get_by_id.format(9999))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Employee not found."})
        mock_get.assert_called_once_with(pk=9999)


    @patch('hr_app.models.Employee.objects.all')
    def test_get_all_employees_success(self, mock_all):
        mock_all.return_value = [
            Employee(**self.employee_data_1),
            Employee(**self.employee_data_2)
        ]
        response = self.client.get(self.url_get_all)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['first_name'], self.employee_data_1['first_name'])
        self.assertEqual(response.data[1]['first_name'], self.employee_data_2['first_name'])
        mock_all.assert_called_once()


    @patch('hr_app.models.Employee.objects.all')
    def test_get_all_employees_empty(self, mock_all):
        mock_all.return_value = []
        response = self.client.get(self.url_get_all)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        mock_all.assert_called_once()