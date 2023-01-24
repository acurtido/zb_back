import pytest
from zb_backend.catalog.models import Brand
from django.contrib.auth.models import User

from rest_framework.test import APIClient

client = APIClient()

@pytest.fixture
def brand():
    return Brand.objects.create(name='test')

@pytest.fixture
def usuario():
    user = User.objects.create(username='a', password='a')
    return user

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def auth_client(usuario, client):
    client.force_authenticate(usuario)
    return client

