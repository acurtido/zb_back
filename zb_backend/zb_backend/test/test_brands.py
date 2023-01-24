import pytest
from zb_backend.catalog.models import Brand
from rest_framework import status

@pytest.mark.django_db
def test_get_brand_service(brand):
    assert brand.name == 'test'

@pytest.mark.django_db
def test_create_brand_service():
    brand = Brand.objects.create(name='test')
    assert brand.name == 'test'

@pytest.mark.django_db
def test_forbidden_create_brand_api(client):
    response = client.post('/brands/', dict(name='xxx'))
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_authenticated_create_brand_api(auth_client):
    response = auth_client.post('/brands/', dict(name='xxx'))
    assert response.status_code == status.HTTP_201_CREATED