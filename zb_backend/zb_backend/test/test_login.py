import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_login():
    response = client.post('/api-auth/login/', dict(username='acurtido', password='acurtido'))
    assert response.status_code == 200
