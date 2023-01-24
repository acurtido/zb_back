import pytest
from zb_backend.catalog.models import Product, Brand

@pytest.mark.django_db
def test_create_product_service():
    product = Product.objects.create(sku='123', name='test', price=10.0, brand=Brand.objects.get_or_create(name='test')[0])
    assert product.sku == '123'