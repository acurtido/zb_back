# Requirements
In order to run this application [Python >= 3.8](https://www.python.org/) should be installed.

# Installation  
1. python3 -m venv env
2. pip install
3. cd zb_backend
4. python manage.py migrate
5. python manage.py loaddata zb_backend/catalog/fixtures/initial_data.json
6. python manage.py createsuperuser --email admin@example.com --username admin
7. python manage.py runserver


