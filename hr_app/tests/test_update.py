from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from ..models import Employee
from decimal import Decimal
from datetime import date

class UpdateEmployeeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/hr_app/employee/update/{}/'
        self.employee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'date_of_birth': date(1985, 5, 15),
            'industry': 'Software Development',
            'salary': Decimal('60000.00'),
            'years_of_experience': 10
        }
        self.employee = Employee.objects.create(**self.employee_data)

    @patch('hr_app.models.Employee.objects.get')
    @patch('hr_app.models.Employee.save')
    def test_update_employee_success(self, mock_save, mock_get):
        mock_get.return_value = self.employee
        update_data = {
            'first_name': 'Jane',
            'industry': 'Marketing',
            'salary': Decimal('65000.00'),
        }
        mock_save.return_value = None
        response = self.client.patch(self.url.format(self.employee.id), update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], update_data['first_name'])
        self.assertEqual(response.data['industry'], update_data['industry'])
        self.assertEqual(response.data['salary'], str(update_data['salary']))
        mock_save.assert_called_once()
        mock_get.assert_called_once_with(pk=self.employee.id)

    @patch('hr_app.models.Employee.objects.get')
    @patch('hr_app.models.Employee.save')
    def test_update_employee_not_found(self, mock_save, mock_get):
        mock_get.side_effect = Employee.DoesNotExist
        update_data = {
            'first_name': 'Jane',
            'industry': 'Marketing',
        }
        response = self.client.patch(self.url.format(9999), update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        mock_save.assert_not_called()
        mock_get.assert_called_once_with(pk=9999)

    @patch('hr_app.models.Employee.objects.get')
    @patch('hr_app.models.Employee.save')
    def test_update_employee_partial_data(self, mock_save, mock_get):
        mock_get.return_value = self.employee
        update_data = {
            'industry': 'Marketing',
        }
        mock_save.return_value = None
        response = self.client.patch(self.url.format(self.employee.id), update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['industry'], update_data['industry'])
        self.assertEqual(response.data['first_name'], self.employee.first_name)
        mock_save.assert_called_once()
        mock_get.assert_called_once_with(pk=self.employee.id)
