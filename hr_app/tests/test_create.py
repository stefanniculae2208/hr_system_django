from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from ..models import Employee
from ..serializers import EmployeeSerializer
from decimal import Decimal
from datetime import date

class AddEmployeeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/hr_app/add/'
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'date_of_birth': date(1985, 5, 15),
            'industry': 'Software Development',
            'salary': Decimal('60000.00'),
            'years_of_experience': 10
        }
        self.invalid_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'date_of_birth': date(1985, 5, 15),
            'industry': 'Software Development',
            'salary': Decimal('60000.00'),
            'years_of_experience': 10
        }

    @patch('hr_app.models.Employee.objects.create')
    def test_add_employee_success(self, mock_create):
        mock_create.return_value = Employee(id=1, **self.valid_data)
        response = self.client.post(self.url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], self.valid_data['first_name'])
        self.assertEqual(response.data['industry'], self.valid_data['industry'])
        mock_create.assert_called_once_with(**self.valid_data)

    @patch('hr_app.models.Employee.objects.create')
    def test_add_employee_invalid_data(self, mock_create):
        mock_create.return_value = None
        response = self.client.post(self.url, self.invalid_data, format='json')

        self.assertEqual(response.status_code, 400)
        mock_create.assert_not_called()
