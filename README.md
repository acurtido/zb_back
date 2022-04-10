# ZB_BACKEND
This app is built with ``Django`` and ``Django Rest Framework``. A showcase can be found deployed at http://zb-backend-env.eba-sd4jik8s.us-west-2.elasticbeanstalk.com/. Password for admin and admin2 is *change123@*.

API documentation can be found at swagger: https://app.swaggerhub.com/apis/acurtido/zb-backend/1.0.0.

# Requirements
In order to run this application [Python >= 3.8](https://www.python.org/) should be installed. This apps uses Django 4, so older version of Python won't work.

# Installation steps
Following the next steps will start the app with a superadmin and some example data.
1. python3 -m venv env
2. pip install
3. cd zb_backend
4. python manage.py migrate
5. python manage.py loaddata zb_backend/catalog/fixtures/initial_data.json
6. python manage.py createsuperuser --email admin@example.com --username admin
7. python manage.py runserver

# AWS SES
If a modification is done in a product, then a notification is sent to other admins by email. This app uses [Amazon Simple Email Service (SES)](https://aws.amazon.com/es/ses/) to send emails to others users with information about the changes. The sender email can be configured in the file settings.py:

``` python
#  file settings.py
EMAIL_SENDER = 'example@mail.com'
```

The email set in this file should be a verified email in AWS SES. If that email is not valid, the app will make the changes but won't notify others admins.

