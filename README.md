python manage.py makemigrations
python manage.py migrate

python manage.py runserver


CURL:

    curl -X POST http://127.0.0.1:8000/api/hr_app/add/ -H "Content-Type: application/json" -d '{"first_name": "Am", "last_name": "Cda", "email": "acrooke0@gizmodo.com", "gender": "M", "date_of_birth": "1978-09-07", "industry": "Other Specialty Stores", "salary": 180466.37, "years_of_experience": 10}'

    curl -X DELETE http://127.0.0.1:8000/api/hr_app/employee/delete/3001/

    curl -X GET "http://127.0.0.1:8000/api/hr_app/employees_filtered/?first_name=Ann&salary_min=100000&sort_by=salary&page=1"

    curl -X GET http://127.0.0.1:8000/api/hr_app/average_age_by_industry/

    curl -X GET http://127.0.0.1:8000/api/hr_app/average_salary_by_industry/

    curl -X GET http://127.0.0.1:8000/api/hr_app/average_salary_by_experience/

    curl -X GET http://127.0.0.1:8000/api/hr_app/gender_distribution_per_industry/

    curl -X GET "http://127.0.0.1:8000/api/hr_app/percentage_above_threshold/?salary_threshold=50000"