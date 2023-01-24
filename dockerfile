FROM python:3.10

COPY zb_backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . code
WORKDIR /code

ENTRYPOINT ["python", "zb_backend/manage.py"]
#CMD ["migrate"]
#CMD ["loaddata ", "zb_backend/catalog/fixtures/initial_data.json"]
#CMD ["createsuperuser", " --email admin@example.com --username acurtido --password acurtido"]
CMD ["runserver", "localhost:8000"]