from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from zb_backend.catalog import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'products-track', views.ProductTrackViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi', get_schema_view(
        title="ZB_Backend API",
        description="API for all things",
        version="1.0.0"
    ), name='openapi-schema'),
]
