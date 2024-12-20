from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from ..models import Employee
from decimal import Decimal
from datetime import date

class DeleteEmployeeTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/hr_app/employee/delete/{}/'  # URL for the DELETE endpoint, where {} will be replaced by the employee ID
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
    @patch('hr_app.models.Employee.delete')  # Mock the delete method
    def test_delete_employee_success(self, mock_delete, mock_get):
        mock_get.return_value = self.employee
        mock_delete.return_value = None
        response = self.client.delete(self.url.format(self.employee.id))
        
        self.assertEqual(response.status_code, 204)
        mock_delete.assert_called_once()
        mock_get.assert_called_once_with(pk=self.employee.id)

    @patch('hr_app.models.Employee.objects.get')
    @patch('hr_app.models.Employee.delete') 
    def test_delete_employee_not_found(self,mock_delete, mock_get):
        mock_get.side_effect = Employee.DoesNotExist
        response = self.client.delete(self.url.format(9999))
        
        self.assertEqual(response.status_code, 404)
        mock_get.assert_called_once_with(pk=9999)
        mock_delete.assert_not_called()
