Dependencies:

        python
        postgresql


General:

        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        
        Setup .env:

                # Docker:
                DB_ENGINE=django.db.backends.postgresql
                DB_NAME=<db_name>
                DB_USER=<user_name>
                DB_PASSWORD=nokia6300
                DB_HOST=dbdjango:5432
                DB_PORT=5432
                DATABASE_URL=postgresql://<user_name>:<user_password>@dbdjango:5432/<db_name>

                # App:
                DB_ENGINE=django.db.backends.postgresql
                DB_NAME=<db_name>
                DB_USER=<user_name>
                DB_PASSWORD=nokia6300
                DB_HOST=localhost
                DB_PORT=5432
                DATABASE_URL=postgresql://<user_name>:<user_password>@localhost/<db_name>


TEST:

        python manage.py test hr_app.tests


APP:

        python manage.py makemigrations
        python manage.py migrate

        python manage.py runserver


DOCKER:

        # Disable SELinux if needed. It was stopping me from running this on my PC.
        sudo setenforce 0
        docker-compose build
        docker-compose up
        sudo docker exec -it django_app /bin/bash
        python manage.py makemigrations
        python manage.py migrate
        exit


CURL:

        curl -X POST http://127.0.0.1:8000/api/hr_app/add/ -H "Content-Type: application/json" -d '{"first_name": "Am", "last_name": "Cda", "email": "acrooke0@gizmodo.com", "gender": "M", "date_of_birth": "1978-09-07", "industry": "Other Specialty Stores", "salary": 180466.37, "years_of_experience": 10}'

        curl -X DELETE "http://127.0.0.1:8000/api/hr_app/employee/delete/3001/" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/employees_filtered/?first_name=Ann&salary_min=100000&sort_by=salary&page=1" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/get_statistics?stat=average_age_by_industry" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/get_statistics?stat=average_salary_by_industry" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/get_statistics?stat=average_salary_by_experience" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/get_statistics?stat=gender_distribution_per_industry" -H "accept: application/json"

        curl -X GET "http://127.0.0.1:8000/api/hr_app/get_statistics?stat=percentage_above_threshold&salary_threshold=50000" -H "accept: application/json"

        curl -X POST "http://127.0.0.1:8000/api/hr_app/upload_employees/" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@data/MOCK_DATA.json"