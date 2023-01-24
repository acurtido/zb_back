# Create your views here.
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from zb_backend.catalog.controllers.aws_ses_controller import send_mail
from zb_backend.catalog.models import Brand, Product, ProductTrack
from zb_backend.catalog.serializers import (BrandSerializer,
                                            ProductSerializer, UserSerializer)
from zb_backend.catalog.serializers import ProductTrackSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    Products management API. 
    
    * Each time a product is queried the number of visits for that product will increase.
    * Every product update made by authenticated users will notify others
    admins by email using [AWS SES][ref].

    [ref]: https://aws.amazon.com/es/ses/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [permissions.AllowAny()]

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        product_track_queryset = ProductTrack.objects.select_for_update().filter(
            product=instance)

        with transaction.atomic():
            product_track = product_track_queryset.first()
            product_track.visits += 1
            product_track.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        users = User.objects.filter()

        for user in users:
            send_mail(recipient=user.email, user=request.user,
                      product=instance)

        return super().update(request, *args, **kwargs)


class ProductTrackViewSet(viewsets.ModelViewSet):
    """
    This API show the total visits for each [product][ref].

    [ref]: /products
    """
    queryset = ProductTrack.objects.all()
    serializer_class = ProductTrackSerializer
    permission_classes = [permissions.IsAuthenticated]
